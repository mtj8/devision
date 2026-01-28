interface Success<T> {
  data: T;
  error?: never;
}
interface Failure<E> {
  data?: never;
  error: E;
}
export type Result<T, E = Error> = Success<T> | Failure<E>;

/** Implements try/catch for a given promise.
 *
 * If the promise resolves, returns an object with a `data` property. If the promise rejects, returns an object with an `error` property.
 * @template E the type of error to return. Defaults to `Error`.
 * @param promise the promise to implement try/catch for.
 * @example
 * const { data, error } = await tryCatch(getData());
 * if (error) return; // handle the error
 * doSomething(data); // data can now be used
 */
async function tryCatch<T, E = Error>(promise: Promise<T>): Promise<Result<T, E>> {
  try {
    const data = await promise;
    return { data };
  } catch (error) {
    return { error: error as E };
  }
}

/** Deserializes a `snake_case` object to `camelCase`. */
function toCamelCase(obj: object) {
  const camelCaseData: object = {};
  for (const key in obj) {
    const camelCaseKey = key.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
    // @ts-expect-error dont care just any
    camelCaseData[camelCaseKey] = obj[key];
  }
  return camelCaseData;
}

/** Serializes a `camelCase` object to `snake_case`. */
function toSnakeCase(obj: object) {
  const snakeCaseData: object = {};
  for (const key in obj) {
    const snakeCaseKey = key.replace(/([A-Z])/g, (_, letter) => `_${letter.toLowerCase()}`);
    // @ts-expect-error dont care just any
    snakeCaseData[snakeCaseKey] = obj[key];
  }
  return snakeCaseData;
}

/** Makes a request to the given endpoint with the given method and body.
 * @param endpoint the endpoint to request. It will be automatically appended to the base URL, **so it should NOT start with a `/`**.
 * @param method the HTTP method to use for the request. Defaults to `"GET"`.
 * @param body the body of the request as an object. It will be automaitcally converted to a `snake_case` JSON object.
 */
async function requestEndpoint(endpoint: string, method?: string, body?: object): Promise<void>;
/** Makes a request to the given endpoint with the given method and body.
 * @template T the type of the request's response
 * @param endpoint the endpoint to request. It will be automatically appended to the base URL, **so it should NOT start with a `/`**.
 * @param method the HTTP method to use for the request. Defaults to `"GET"`.
 * @param body the body of the request as an object. It will be automaitcally converted to a `snake_case` JSON object.
 * @returns the JSON response from the request. If it is an object, it will be converted to `camelCase`.
 */
async function requestEndpoint<T>(endpoint: string, method?: string, body?: object): Promise<T>;
async function requestEndpoint<T>(endpoint: string, method?: string, body?: object): Promise<T | void> {
  const config = useRuntimeConfig();

  const options: RequestInit = { credentials: "include" };
  if (method) {
    options.method = method;
    options.headers = { "Content-Type": "application/json" };
    options.body = JSON.stringify(typeof body !== "object" || Array.isArray(body) ? body : toSnakeCase(body));
  }

  const res = await fetch(config.public.backend + endpoint, options);
  if (!res.ok) throw new Error(res.statusText);

  const contentLength = res.headers.get("Content-Length");
  if (contentLength === "0") return undefined as T;

  const data = await res.json();
  return (typeof data !== "object" || Array.isArray(data) ? data : toCamelCase(data)) as T;
}

/** **Serves as a wrapper for `tryCatch(requestEndpoint())`.**
 * @param endpoint the endpoint to request. It will be automatically appended to the base URL, **so it should NOT start with a `/`**.
 * @param method the HTTP method to use for the request. Defaults to `"GET"`.
 * @param body the body of the request as an object. It will be automaitcally converted to a `snake_case` JSON object.
 */
export async function fetchEndpoint(endpoint: string, method?: string, body?: object): Promise<Result<void>>;
/** **Serves as a wrapper for `tryCatch(requestEndpoint())`.**
 * @template T the type of the request's response
 * @param endpoint the endpoint to request. It will be automatically appended to the base URL, **so it should NOT start with a `/`**.
 * @param method the HTTP method to use for the request. Defaults to `"GET"`.
 * @param body the body of the request as an object. It will be automaitcally converted to a `snake_case` JSON object.
 * @returns the JSON response from the request. If it is an object, it will be converted to `camelCase`.
 */
export async function fetchEndpoint<T, K = Error>(endpoint: string, method?: string, body?: object): Promise<Result<T, K>>;
export async function fetchEndpoint<T, K = Error>(endpoint: string, method?: string, body?: object): Promise<Result<T | void, K>> {
  return tryCatch<T, K>(requestEndpoint<T>(endpoint, method, body));
}
