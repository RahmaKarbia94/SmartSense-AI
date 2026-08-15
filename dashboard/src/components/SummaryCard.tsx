interface SummaryCardProps {
  label: string;
  value: string;
}

export function SummaryCard({ label, value }: SummaryCardProps) {
  return (
    <div className="summary-card">
      <span className="summary-card__label">{label}</span>
      <span className="summary-card__value">{value}</span>
    </div>
  );
}