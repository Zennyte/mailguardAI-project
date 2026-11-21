import FormField from "./FormField";

// Dropdown me etikete.
// "options" eshte nje liste {value, title} (shiko src/config/dropdownOptions.js)
// dhe onChange merr direkt vleren e zgjedhur: onChange={setListName}
function SelectField({ label, value, onChange, options, className = "" }) {
  return (
    <FormField label={label} className={className}>
      <select
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className="input-field"
      >
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.title}
          </option>
        ))}
      </select>
    </FormField>
  );
}

export default SelectField;
