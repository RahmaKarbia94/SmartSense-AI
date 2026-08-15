const OPTIONS = [10, 25, 50, 100] as const;

interface TimeRangeSelectorProps {
  value: number;
  onChange: (value: number) => void;
}

export function TimeRangeSelector({ value, onChange }: TimeRangeSelectorProps) {
  return (
    <div className="time-range-selector">
      {OPTIONS.map((option) => (
        <button
          key={option}
          type="button"
          className={option === value ? "time-range-selector__button--active" : ""}
          onClick={() => onChange(option)}
        >
          Last {option}
        </button>
      ))}
    </div>
  );
}