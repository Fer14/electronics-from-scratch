# Phase 20: Chip Design

> Designing a chip is spending a budget of area, energy and time between computing and moving data.

You already know what a gate is (Phase 14), how registers and clocks work (Phase 15), what a processor does (Phase 16) and how a microcontroller is used (Phase 17). This phase asks why real chips, and especially AI chips, look the way they do. One idea runs through every lesson: a chip designer has three currencies (silicon area, energy and time), and must split them between doing arithmetic and moving numbers to where the arithmetic happens. We extend our logic simulator with a cost model (`sim.cost`) in which every block reports its area in gates, its delay in gate delays and the bits it moves, and we use it to build and compare adders, multipliers, MACs, pipelines, systolic arrays, memories and whole chips. Along the way we meet the facts that shape modern hardware: multipliers grow with the square of their width, fetching a number costs far more than multiplying it, feedback loops limit the clock, batching moves a model from memory-bound to compute-bound, and big dies cost much more than their area suggests. It is also the bridge to *Deep Learning from Scratch*: here you see in silicon why precision, batching and the KV cache matter.

**Prerequisites:** Phase 14 (Digital Logic), Phase 15 (Sequential Logic), Phase 16 (A Computer from Gates); Phase 17 (Microcontrollers) helps for context.

| # | Lesson | What you learn |
|---|--------|----------------|
| 01 | [From Gates to Adders](01-from-gates-to-adders/) | Counting area and delay by hand, ripple adders that grow linearly, a carry-select adder that buys speed with area |
| 02 | [Multiplying in Hardware](02-multiplying-in-hardware/) | Partial products, the array multiplier, half-adder trimming, area that grows with the square of the width |
| 03 | [The MAC](03-the-mac/) | Matrix products as multiply-accumulates, accumulator width and overflow, a clocked MAC from gates |
| 04 | [Moving Data Costs More](04-moving-data-costs-more/) | Energy per operation vs per access, wire energy from C V^2, register-file area, reuse |
| 05 | [Clocks, Critical Paths and Pipelining](05-clocks-critical-paths-and-pipelining/) | Clock period from the critical path, pipeline registers, throughput vs latency, the loop that cannot be cut |
| 06 | [Systolic Arrays](06-systolic-arrays/) | A weight-stationary array simulated cycle by cycle, skew, utilization, compute on the area and data on the edge |
| 07 | [Memory on the Chip](07-memory-on-the-chip/) | SRAM, DRAM and HBM, an LRU cache vs a scratchpad, tiling, splitting area between MACs and buffer |
| 08 | [The Roofline](08-the-roofline/) | Arithmetic intensity, the ridge point, batch size vs throughput and latency, why decode is memory-bound |
| 09 | [FPGA and ASIC](09-fpga-and-asic/) | Lookup tables built from multiplexers, the cost of programmability, break-even volume |
| 10 | [CPU, GPU and Accelerators](10-cpu-gpu-and-accelerators/) | Where each spends its area, number formats from fp32 to fp4, scaling, outliers, wide accumulators |
| 11 | [From RTL to the Fab](11-from-rtl-to-the-fab/) | Verilog, a toy synthesizer and placer, tape-out, dies per wafer, yield, chiplets |

Labs in this phase:

- 01 · Finish the 4-bit adder (logic)
- 02 · Trim the 4x4 multiplier to 64 gates (logic)
- 03 · Size the accumulator (chip)
- 05 · Pipeline the datapath to meet the clock (chip)
- 07 · Split the area between MACs and memory (chip)
- 08 · Pick the batch that makes the layer compute-bound (chip)
- 09 · Program the LUT as a majority vote (logic)

Run the first lesson:

```
uv run python phases/20-chip-design/01-from-gates-to-adders/code/main.py
```
