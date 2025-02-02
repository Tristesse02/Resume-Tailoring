export function Input({ value, onChange, placeholder }) {
  return (
    <input
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      className="border border-gray-300 p-2 rounded w-full"
    />
  );
}
