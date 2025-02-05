from dotenv import load_dotenv  # import load_dotenv function

from googleapiclient.discovery import build  # the main function to build the service
from google.oauth2.service_account import Credentials  # the credentials object

load_dotenv()

# Load credentials from the JSON file
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
]
creds = Credentials.from_service_account_file("configs/credentials.json", scopes=SCOPES)

# Initialize Google Docs and Drive services
docs_service = build("docs", "v1", credentials=creds)
drive_service = build("drive", "v3", credentials=creds)


# Function to copy a template Google Doc
def copy_template(template_id, new_title):
    body = {"name": new_title}
    copied_file = drive_service.files().copy(fileId=template_id, body=body).execute()
    return copied_file["id"]


def replace_placeholders(doc_id, replacements):
    """
    Replace placeholders in the document with provided text.

    Args:
        doc_id (_type_): _description_
        replacements (_type_): _description_
    """
    requests = []
    for placeholder, value in replacements.items():
        replace_text = value["text"] if isinstance(value, dict) else value
        requests.append(
            {
                "replaceAllText": {
                    "containsText": {
                        "text": f"{{{{{placeholder}}}}}",
                        "matchCase": True,
                    },
                    "replaceText": replace_text,
                }
            }
        )

        # Execute place holder replacements
        docs_service.documents().batchUpdate(
            documentId=doc_id, body={"requests": requests}
        ).execute()


def get_next_start_index_in_table(doc_id, placeholder):
    """
    Find the endIndex of the last element in the table cell containing the placeholder.
    This will be the start index for the next bullet point.

    Args:
        doc_id (str): The Google Doc ID.
        placeholder (str): The placeholder to locate (e.g., {{Company1Content}}).

    Returns:
        int: The start index for the next bullet point.
    """
    # Get the document content
    document = docs_service.documents().get(documentId=doc_id).execute()
    content = document.get("body").get("content")

    # Traverse the document content to find tables
    for element in content:
        if "table" in element:
            table = element["table"]
            for row in table["tableRows"]:
                for cell in row["tableCells"]:
                    for cell_content in cell["content"]:
                        if "paragraph" in cell_content:
                            for paragraph_element in cell_content["paragraph"][
                                "elements"
                            ]:
                                text_run = paragraph_element.get("textRun")
                                if text_run and placeholder in text_run.get(
                                    "content", ""
                                ):
                                    print(f"Found placeholder: {placeholder}")
                                    # Return the endIndex of the last element in the cell
                                    return cell_content["endIndex"]

    print(f"Placeholder '{placeholder}' not found in the table.")
    return None


# def replace_and_print_bullet_content_in_table(doc_id, placeholder, new_content):
#     """
#     Replace a placeholder with new content and print the object containing the bullet point.

#     Args:
#         doc_id (str): The ID of the Google Doc.
#         placeholder (str): The placeholder to replace (e.g., {{Company1Content}}).
#         new_content (str): The content to replace the placeholder with.
#     """
#     # Get the document content
#     document = docs_service.documents().get(documentId=doc_id).execute()
#     content = document.get("body").get("content")

#     # Traverse the document content to find tables
#     for element in content:
#         if "table" in element:
#             table = element["table"]
#             for row in table["tableRows"]:
#                 for cell in row["tableCells"]:
#                     for cell_content in cell["content"]:
#                         if "paragraph" in cell_content:
#                             for paragraph_element in cell_content["paragraph"][
#                                 "elements"
#                             ]:
#                                 text_run = paragraph_element.get("textRun")
#                                 if text_run and placeholder in text_run.get(
#                                     "content", ""
#                                 ):
#                                     print(f"Found placeholder: {placeholder}")

#                                     # Replace the placeholder with the new content
#                                     requests = [
#                                         {
#                                             "replaceAllText": {
#                                                 "containsText": {
#                                                     "text": placeholder,
#                                                     "matchCase": True,
#                                                 },
#                                                 "replaceText": new_content,
#                                             }
#                                         }
#                                     ]
#                                     docs_service.documents().batchUpdate(
#                                         documentId=doc_id, body={"requests": requests}
#                                     ).execute()

#                                     # Print the updated table cell object
#                                     print("Updated object containing the bullet point:")
#                                     print(cell_content)
#                                     return

#     print(f"Placeholder '{placeholder}' not found in the table.")


def create_second_bullet_point(
    doc_id, first_bullet_config, new_placeholder, start_index
):
    """
    Create a second bullet point with the same configuration as the first bullet.

    Args:
        doc_id (str): The Google Doc ID.
        first_bullet_config (dict): The configuration of the first bullet point (listId, textStyle).
        new_placeholder (str): The placeholder for the second bullet content.
        start_index (int): The index to insert the second bullet point.
    """
    # Extract the listId and textStyle from the first bullet's configuration
    list_id = first_bullet_config["listId"]
    text_style = first_bullet_config["textStyle"]

    # Prepare the requests to insert the second bullet
    requests = [
        # Insert the placeholder text for the new bullet
        {
            "insertText": {
                "location": {
                    "index": start_index,
                },
                "text": new_placeholder + "\n",  # Add a newline for the bullet point
            }
        },
        # Create a bullet point with the same listId as the first bullet
        {
            "createParagraphBullets": {
                "range": {
                    "startIndex": start_index,
                    "endIndex": start_index
                    + len(new_placeholder)
                    + 1,  # Include the newline
                },
                "listId": list_id,  # Use the same bullet style as the first bullet
            }
        },
        # Apply the same text style as the first bullet
        {
            "updateTextStyle": {
                "range": {
                    "startIndex": start_index,
                    "endIndex": start_index
                    + len(new_placeholder)
                    + 1,  # Include the newline
                },
                "textStyle": text_style,  # Apply the text style from the first bullet
                "fields": ",".join(text_style.keys()),  # Specify which fields to apply
            }
        },
    ]

    # Execute the batch update request
    docs_service.documents().batchUpdate(
        documentId=doc_id, body={"requests": requests}
    ).execute()

    print(f"Added second bullet point with placeholder: {new_placeholder}")


def add_hyperlinks(doc_id, replacements):
    """
    Adds hyperlinks to text specified in the replacements

    Args:
        doc_id (_type_): _description_
        replacements (_type_): _description_
    """

    # Get the document's content
    document = docs_service.documents().get(documentId=doc_id).execute()
    content = document.get("body").get("content")

    # create requests to add links
    requests = []
    for placeholder, value in replacements.items():
        if isinstance(value, dict) and "text" in value and "link" in value:
            text_to_find = value["text"]
            link_url = value["link"]

            # Find the range of the replaced text
            start_index, end_index = find_text_range(content, text_to_find)
            if start_index is not None and end_index is not None:
                requests.append(
                    {
                        "updateTextStyle": {
                            "range": {"startIndex": start_index, "endIndex": end_index},
                            "textStyle": {"link": {"url": link_url}},
                            "fields": "link",
                        }
                    }
                )

    # Execute hyperlink requests
    if requests:
        docs_service.documents().batchUpdate(
            documentId=doc_id, body={"requests": requests}
        ).execute()


def find_text_range(content, text_to_find):
    """
    Finds the range of the specified text in the document.

    Args:
        content (list): Document content
        text_to_find (str): Text to search for

    Returns:
        Tuple[int, int]: Start and end indices of the text, or (None, None) if not found
    """
    for element in content:
        if "paragraph" in element:
            for paragraph_element in element["paragraph"]["elements"]:
                text_run = paragraph_element.get("textRun")
                if text_run and "content" in text_run:
                    text = text_run["content"]
                    start_index = paragraph_element.get("startIndex", -1)
                    if text_to_find in text:
                        # Calculate the exact start and end indices
                        match_start = text.index(text_to_find)
                        actual_start_index = start_index + match_start
                        actual_end_index = actual_start_index + len(text_to_find)
                        return actual_start_index, actual_end_index
    return None, None  # Text not found


def test_file_access():
    print("Listing accessible files for the service account:")
    results = drive_service.files().list(pageSize=10).execute()
    for file in results.get("files", []):
        print(f"Found file: {file.get('name')} (ID: {file.get('id')})")


def share_file_with_user(file_id, user_email):
    # Create a permission object
    permission = {
        "type": "user",
        "role": "writer",
        "emailAddress": user_email,
    }

    # Insert the permission
    drive_service.permissions().create(
        fileId=file_id, body=permission, fields="id"
    ).execute()

    print(f"Shared file {file_id} with {user_email}")


if __name__ == "__main__":
    # Copy the template
    TEMPLATE_ID = "1NnPMKqj6NN4i_qsqsHaPEcz3WxEBNBrApXGg7zwd_IE"
    new_doc_id = copy_template(TEMPLATE_ID, "Custom Resume")

    previous_bullet = {
        "listId": "kix.list.1",  # Extracted from the first bullet's configuration
        "textStyle": {  # Extracted from the first bullet's text style
            "fontSize": {"magnitude": 10, "unit": "PT"},
            "weightedFontFamily": {"fontFamily": "Times New Roman", "weight": 400},
        },
    }

    # Replace placeholders
    placeholders = {
        "Name": "Minh Vu",
        "Email": {"text": "mtvu@umass.edu", "link": "mailto:mtvu@umass.edu"},
        "Phone": "+1 (413) 275 6387",
        "LinkedIn": {
            "text": "linkedin.com/in/minhvu02/",
            "link": "https://www.linkedin.com/in/minhvu02/",
        },
        "Github": {
            "text": "github.com/Tristesse02",
            "link": "https://github.com/Tristesse02",
        },
        "Company1": "Avocademy",
    }

    bullet_points = [
        "Leveraged OpenAI API to engineer a job classification system delivering tailored recommendations, boosting job relevance by 50%.",
        "Utilized React and SpringBoot to develop an auto tailored job application using serverless and microservice architecture.",
        "Streamlined the extraction of 750+ daily job postings and automated applications using Fire Crawler, PuppeteerJS, and Playwright.",
        "Managed 70,000+ database entries to efficiently monitor job posting, user data, and platform activity using MongoDB and Supabase.",
        # "Set up GitHub CI/CD pipeline for A/B and E2E testing and deployment on Vercel, increasing customer satisfaction by 30%.",
        "I swear to god that Im so handsome",
    ]

    start_index = get_next_start_index_in_table(new_doc_id, "{{Company1Content}}")

    if start_index is not None:
        new_placeholders = "{{Company1Contentlvvllvvl}}"

        # Create the second bullet point
        create_second_bullet_point(
            doc_id=new_doc_id,
            first_bullet_config=previous_bullet,
            new_placeholder=new_placeholders,
            start_index=start_index,
        )

    # replace_placeholders(new_doc_id, placeholders)
    # add_hyperlinks(new_doc_id, placeholders)

    print(f"New document created: https://docs.google.com/document/d/{new_doc_id}/edit")

    # Share the file with your personal Google account
    personal_email = "tienminhvu2107@gmail.com"
    share_file_with_user(new_doc_id, personal_email)
    # test_file_access()
    # # Id of your template Google Doc

    # # Copy the template
    # new_doc_id = copy_template(TEMPLATE_ID, "Custom Resume")
