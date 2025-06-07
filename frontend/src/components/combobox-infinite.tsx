import { useState, useEffect, useRef } from "react";
import { Check, ChevronsUpDown } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Skeleton } from "@/components/ui/skeleton";

interface Option {
  id: string | number;
  label: string;
}

interface Props {
  value: Option | null;
  onChange: (value: Option | null) => void;
  options: Option[];
  onSearch: (query: string) => void;
  onLoadMore: () => void;
  hasNextPage: boolean;
  isFetchingNextPage: boolean;
  placeholder?: string;
}

export function ComboBoxInfinite({
  value,
  onChange,
  options,
  onSearch,
  onLoadMore,
  hasNextPage,
  isFetchingNextPage,
  placeholder = "Buscar...",
}: Props) {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");

  const listRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = listRef.current;
    if (!el) return;

    const handleScroll = () => {
      if (
        el.scrollTop + el.clientHeight >= el.scrollHeight - 10 &&
        hasNextPage &&
        !isFetchingNextPage
      ) {
        onLoadMore();
      }
    };

    el.addEventListener("scroll", handleScroll);
    return () => el.removeEventListener("scroll", handleScroll);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [hasNextPage, isFetchingNextPage]);

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          aria-expanded={open}
          className="w-full justify-between"
        >
          {value ? value.label : placeholder}
          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="p-0 w-full">
        <Command shouldFilter={false}>
          <CommandInput
            placeholder={placeholder}
            className="h-9"
            value={query}
            onValueChange={(text) => {
              setQuery(text);
              onSearch(text);
            }}
          />
          <CommandList ref={listRef}>
            <CommandEmpty>No hay resultados.</CommandEmpty>
            <CommandGroup>
              {options.map((item) => (
                <CommandItem
                  key={item.id}
                  value={item.label}
                  onSelect={() => {
                    onChange(item);
                    setQuery(item.label);
                    setOpen(false);
                  }}
                >
                  {item.label}
                  <Check
                    className={cn(
                      "ml-auto h-4 w-4",
                      value?.id === item.id ? "opacity-100" : "opacity-0"
                    )}
                  />
                </CommandItem>
              ))}
              {isFetchingNextPage && (
                <div className="px-4 py-2">
                  <Skeleton className="h-4 w-full mb-1" />
                  <Skeleton className="h-4 w-full" />
                </div>
              )}
              {!hasNextPage && !isFetchingNextPage && options.length > 0 && (
                <div className="text-center text-xs text-muted-foreground py-2">
                  Fin de resultados
                </div>
              )}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  );
}
