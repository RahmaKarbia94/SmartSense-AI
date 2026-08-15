import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { SummaryCard } from "./SummaryCard";

describe("SummaryCard", () => {
  it("renders the label and value", () => {
    render(<SummaryCard label="Temperature" value="25.34 °C" />);
    expect(screen.getByText("Temperature")).toBeInTheDocument();
    expect(screen.getByText("25.34 °C")).toBeInTheDocument();
  });
});