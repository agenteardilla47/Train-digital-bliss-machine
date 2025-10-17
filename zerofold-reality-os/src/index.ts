export type Event = { id: string; t: number; type: string; payload: unknown };
export type State = Record<string, unknown>;
export type Reducer = (state: State, event: Event) => State;

export class RealityKernel {
  private readonly events: Event[] = [];
  constructor(private readonly reduce: Reducer) {}

  append(event: Event): void {
    this.events.push(event);
  }

  fork(untilT?: number): RealityBranch {
    const cut = untilT ?? Number.POSITIVE_INFINITY;
    const forkLog = this.events.filter((e) => e.t <= cut);
    return new RealityBranch(forkLog, this.reduce);
  }
}

export class RealityBranch {
  constructor(private readonly log: Event[], private readonly reduce: Reducer) {}

  state(): State {
    return [...this.log]
      .sort((a, b) => (a.t === b.t ? a.id.localeCompare(b.id) : a.t - b.t))
      .reduce(this.reduce, {} as State);
  }

  retroInsert(event: Event): void {
    this.log.push(event);
  }

  diff(other: RealityBranch): Event[] {
    const thisIds = new Set(this.log.map((e) => e.id));
    return other.log.filter((e) => !thisIds.has(e.id));
  }

  merge(other: RealityBranch): RealityBranch {
    const merged = [...this.log, ...this.diff(other)].sort((a, b) =>
      a.t === b.t ? a.id.localeCompare(b.id) : a.t - b.t,
    );
    return new RealityBranch(merged, this.reduce);
  }
}
