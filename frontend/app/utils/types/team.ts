export interface Team {
  readonly uuid: string;
  /** Name of the team. */
  readonly name: string;
  /** When the team was created.
   * @warning Must be parsed from a unix timestamp in seconds
   */
  readonly createdAt: Date;
  /** Array of users on the team. */
  readonly members: PublicUser[];
}

export interface TeamProfile extends Team {
  /** The hackathon that the team performed best in, if the team has participated in any hackathons. */
  readonly bestPlacement: MinifiedHackathon | null;
  /** 5 of the team's most recently completed hackathons. */
  readonly pastHackathons: MinifiedHackathon[];
}
