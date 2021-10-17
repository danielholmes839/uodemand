import {
  ApolloClient,
  InMemoryCache,
  createHttpLink,
  DefaultOptions,
} from "@apollo/client";

const port = 8000;
const host = `http://localhost:${port}`;

const defaultOptions: DefaultOptions = {
  mutate: {
    fetchPolicy: "no-cache",
  },
};

const httpLink = createHttpLink({
  uri: `${host}/api/graphql`,
});

export const client = new ApolloClient({
  link: httpLink,
  cache: new InMemoryCache(),
  defaultOptions: defaultOptions,
});
