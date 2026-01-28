export interface SidebarLink {
  /** Name of the link. */
  readonly name: string;
  /** Path to the link's icon, from the /public directory. */
  readonly icon: string;
  /** Path of the link. */
  readonly path: string;
  /** Custom active test function for the link, if needed. */
  readonly customActiveTest?: () => boolean;
}

export * from "./types/user";
export * from "./types/team";
export * from "./types/hackathon";
