/**
 * @typedef {Object} FormData
 * @property {string} name - The name of the project or work experience.
 * @property {string} type - Type of the entry (e.g., 'Project' or 'Work Experience').
 * @property {string} techStack - Comma-separated list of technologies used.
 * @property {string} description - A short description of the project or job role.
 * @property {string} numbers - Quantifiable metrics related to the entry.
 * @property {string} bulletPoints - Key bullet points for achievements.
 */

/**
 * @typedef {Object} ResumeEntry
 * @property {string} title - Title of the project/work experience.
 * @property {string} type - Category (either 'Project' or 'Work Experience').
 * @property {string[]} techStack - Array of technologies used.
 * @property {string} description - Description of the work done.
 * @property {string} quantifiableMetrics - Relevant numerical data.
 * @property {string} bulletPoints - Key bullet points.
 */

/**
 * @typedef {Object} ResumeData
 * @property {ResumeEntry[]} [personal_projects] - List of personal projects.
 * @property {ResumeEntry[]} [work_experiences] - List of work experiences.
 */

/**
 * @typedef {Object} ResumeRequest
 * @property {ResumeData} resume_data - The structured resume entries.
 * @property {string} job_description - The job description from the user.
 */

export {};
