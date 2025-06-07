import { FormControl } from "./ui/form";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./ui/select";

interface SelectFieldProps {
  value: string;
  onChange: (value: string) => void;
  options: { value: string; label: string }[];
}

export const SelectField = ({ value, onChange, options }: SelectFieldProps) => {
  return (
    <Select onValueChange={onChange} value={value}>
      <FormControl>
        <SelectTrigger className="w-full">
          <SelectValue placeholder="Seleccione un rol" />
        </SelectTrigger>
      </FormControl>
      <SelectContent>
        {options.map((option) => (
          <SelectItem key={option.value} value={option.value}>
            {option.label}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
};
