import { RealityKernel, Reducer, Event } from "../index.js";

const reducer: Reducer = (state, event) => {
  if (event.type === "add") {
    const key = String((event.payload as any).key);
    const value = (event.payload as any).value;
    return { ...state, [key]: value };
  }
  return state;
};

const k = new RealityKernel(reducer);

const events: Event[] = [
  { id: "e1", t: 1, type: "add", payload: { key: "x", value: 1 } },
  { id: "e2", t: 2, type: "add", payload: { key: "y", value: 2 } },
];

for (const e of events) k.append(e);

const b1 = k.fork();
console.log("state@b1", b1.state());

const b2 = k.fork();
b2.retroInsert({ id: "e0", t: 0, type: "add", payload: { key: "z", value: 0 } });
console.log("state@b2", b2.state());

const merged = b1.merge(b2);
console.log("state@merged", merged.state());
