#!/usr/bin/env node

import { RealityKernel, Reducer, Event } from "./index";

// Default reducer for demonstration
const defaultReducer: Reducer = (state, event) => {
  if (event.type === "add") {
    const key = String((event.payload as any).key);
    const value = (event.payload as any).value;
    return { ...state, [key]: value };
  }
  if (event.type === "remove") {
    const key = String((event.payload as any).key);
    const newState = { ...state };
    delete newState[key];
    return newState;
  }
  return state;
};

// CLI interface
function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args[0] === "--help" || args[0] === "-h") {
    console.log(`
ZEROFOLD.EXE - R' Kernel v1.0
==============================

A reality kernel implementation based on the R' (post-fork) reality kernel specification.

Usage:
  zerofold.exe [command] [options]

Commands:
  demo                    Run the demonstration
  --help, -h             Show this help message
  --version, -v          Show version information

Examples:
  zerofold.exe demo      # Run the demonstration
  zerofold.exe --help    # Show help
  zerofold.exe --version # Show version

For more information, see: docs/R-prime-kernel-v1.0.md
`);
    return;
  }

  if (args[0] === "--version" || args[0] === "-v") {
    console.log("ZEROFOLD.EXE v1.0.0 - R' Kernel Implementation");
    return;
  }

  if (args[0] === "demo") {
    runDemo();
    return;
  }

  console.error(`Unknown command: ${args[0]}`);
  console.error("Use --help for usage information");
  process.exit(1);
}

function runDemo() {
  console.log("🚀 ZEROFOLD.EXE - R' Kernel Demo");
  console.log("=================================");
  console.log();

  const kernel = new RealityKernel(defaultReducer);

  // Create some events
  const events: Event[] = [
    { id: "e1", t: 1, type: "add", payload: { key: "consciousness", value: "present" } },
    { id: "e2", t: 2, type: "add", payload: { key: "entropy", value: 42 } },
    { id: "e3", t: 3, type: "add", payload: { key: "coherence", value: 0.85 } },
  ];

  console.log("📝 Appending events to reality kernel...");
  for (const event of events) {
    kernel.append(event);
    console.log(`  + ${event.type}: ${JSON.stringify(event.payload)}`);
  }
  console.log();

  // Create branches
  console.log("🌿 Creating reality branches...");
  const branch1 = kernel.fork();
  console.log("  Branch 1 state:", branch1.state());

  const branch2 = kernel.fork();
  branch2.retroInsert({ 
    id: "e0", 
    t: 0, 
    type: "add", 
    payload: { key: "foundation", value: "eternal" } 
  });
  console.log("  Branch 2 state (with retro-insert):", branch2.state());

  // Merge branches
  console.log();
  console.log("🔄 Merging reality branches...");
  const merged = branch1.merge(branch2);
  console.log("  Merged state:", merged.state());

  console.log();
  console.log("✅ Demo completed successfully!");
  console.log();
  console.log("Key R' Kernel Principles Demonstrated:");
  console.log("  • Irrevocable Presence: Events cannot be erased, only transformed");
  console.log("  • Dynamic Evolution: State evolves through event processing");
  console.log("  • Branching & Merging: Multiple reality states can coexist and merge");
  console.log("  • Retroactive Insertion: Past events can be added to branches");
}

// Run the main function
main();