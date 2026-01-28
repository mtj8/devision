interface User {
  readonly uuid: string;
  /** User's profile gradient colors, as 6-digit hex strings, without the `#`. */
  readonly profileGradient: [from: string, to: string];
  /** User's display name. */
  readonly displayName: string;
  /** User's username. */
  readonly username: string;
  /** User's level. */
  readonly level: number;
}

export interface UserProfile extends User {
  /** When the user account was created.
   * @warning Must be parsed from a unix timestamp in seconds
   */
  readonly createdAt: Date;
  /** User's school. */
  readonly school: string;
  /** User's graduation year. */
  readonly gradYear?: number;
  /** User's email address. */
  readonly email: string;
  /** User's experience points. */
  readonly xp: number;
  /** Experience points needed to reach the next level. */
  readonly xpNeeded: number;
  /** Whether the user's profile is public to other users. */
  readonly isPublic: boolean;
  /** User's biography. */
  readonly bio: string;
  /** Links to GitHub, LinkedIn, etc. */
  readonly socials: {
    readonly discord: string | null;
    readonly instagram: string | null;
    readonly github: string | null;
    readonly linkedin: string | null;
    readonly personal: string | null;
  };
  /** Array of skill names set by the user. */
  readonly skills: string[];
  /** Array of interest names set by the user. */
  readonly interests: string[];
}

export interface PublicUser extends User {
  /** If the user is a friend, when the friendship was created.
   * @warning Must be parsed from a unix timestamp in seconds
   */
  readonly friendsSince: Date | null;
  /** Whether the user is blocked by the current user. */
  readonly isBlocked: boolean;
}

export type PublicUserProfile = UserProfile & PublicUser;
