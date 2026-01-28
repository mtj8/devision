interface BaseHackathon {
  readonly uuid: string;
  /** Name of the hackathon. */
  readonly name: string;
  /** Description of the hackathon. */
  readonly description: string;
  /** Start date of the hackathon.
   * @warning Must be parsed from a unix timestamp in seconds
   */
  readonly startDate: Date;
  /** End date of the hackathon.
   * @warning Must be parsed from a unix timestamp in seconds
   */
  readonly endDate: Date;
  /** Number of participants in the hackathon. */
  readonly participants: number;
}

export interface Hackathon extends BaseHackathon {
  /** Team of the user in the hackathon, if any */
  readonly team?: Team;
}

export interface HackathonProfile extends Hackathon {
  /** Top 10 teams in the hackathon. */
  readonly leaderboard: Team[];
  /** Team's placement in the hackathon, if any. */
  readonly placement: number | null;
}

export interface MinifiedHackathon extends BaseHackathon {
  /** Team's placement in the hackathon. */
  readonly placement: number;
}
