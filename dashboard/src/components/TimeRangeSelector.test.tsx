import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { TimeRangeSelector } from "./TimeRangeSelector";

describe("TimeRangeSelector", () => {
  it("calls onChange with the selected value", async () => {
    const onChange = vi.fn();
    render(<TimeRangeSelector value={25} onChange={onChange} />);

    await userEvent.click(screen.getByText("Last 50"));

    expect(onChange).toHaveBeenCalledWith(50);
  });

  it("marks the current value as active", () => {
    render(<TimeRangeSelector value={50} onChange={() => {}} />);
    expect(screen.getByText("Last 50")).toHaveClass(
      "time-range-selector__button--active"
    );
  });
});