interface BaseUser {
  readonly uuid: string;
  /** User's profile gradient colors, as 6-digit hex strings, without the `#`. */
  readonly profileGradient: [from: string, to: string];
  /** User's display name. */
  readonly displayName: string;
  /** User's username. */
  readonly username: string;
  /** When the user account was created.
   * @warning Must be parsed from a unix timestamp in seconds
   */
  readonly createdAt: Date;
  /** User's school. */
  readonly school: string;
  /** User's graduation year. */
  readonly gradYear: number;
  /** User's major. */
  readonly major: string;
  /** If the user is a friend, when the friendship was created.
   * @warning Must be parsed from a unix timestamp in seconds
   */
  readonly friendsSince: Date | null;
  /** Whether the user is blocked by the current user. */
  readonly isBlocked: boolean;
}

interface BasePublicUser extends BaseUser {
  /** Whether the user's profile is public to other users. */
  readonly isPublic: true;
  /** User's email address. */
  readonly email: string;
  /** User's level. */
  readonly level: number;
  /** User's experience points. */
  readonly xp: number;
  /** Remaining experience points needed to reach the next level. */
  readonly xpNeeded: number;
  /** User's biography. */
  readonly bio: string;
  /** Links to GitHub, LinkedIn, etc. */
  readonly socials: {
    /** Discord username */
    readonly discord: string | null;
    /** Instagram username */
    readonly instagram: string | null;
    /** GitHub username */
    readonly github: string | null;
    /** LinkedIn profile URL */
    readonly linkedin: string | null;
    /** Personal website URL */
    readonly personal: string | null;
  };
  /** Array of skill names set by the user. */
  readonly skills: string[];
  /** Array of interest names set by the user. */
  readonly interests: string[];
}

interface BasePrivateUser extends BaseUser {
  /** Whether the user's profile is public to other users. */
  readonly isPublic: false;
}

/** @template T `true` if the user is public, `false` if private. If ommitted, refers to any type of user. */
export type User<T extends boolean | null = null> = T extends null ? BasePublicUser | BasePrivateUser : T extends true ? BasePublicUser : BasePrivateUser;
/** Alias for `User<true>`. */
export type PublicUser = User<true>;
/** Alias for `User<false>`. */
export type PrivateUser = User<false>;
