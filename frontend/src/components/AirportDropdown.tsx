type Airport = {
  airport: string;
  city: string;
};

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

function AirportDropdown({
  airports,
  selected,
  onSelect,
}: {
  airports: Airport[];
  selected: Airport | null;
  onSelect: (airport: Airport) => void;
}) {
  return (
    <div className="flex flex-col items-center justify-center">
      <DropdownMenu>
        <DropdownMenuTrigger className="bg-gray-200 px-4 py-2 rounded-md min-w-[200px] text-left">
          {selected ? selected.city : "Select Airport"}
        </DropdownMenuTrigger>
        <DropdownMenuContent>
          {airports.length > 0 ? (
            airports.map((airport) => (
              <DropdownMenuItem
                key={airport.airport}
                onClick={() => onSelect(airport)}
              >
                {airport.city}
              </DropdownMenuItem>
            ))
          ) : (
            <DropdownMenuItem disabled>No airports available</DropdownMenuItem>
          )}
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
}

export default AirportDropdown;
