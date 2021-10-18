import {
  ApolloClient,
  InMemoryCache,
  createHttpLink,
  DefaultOptions,
} from "@apollo/client";

const uri =
  process.env.NODE_ENV === "production"
    ? `http://localhost:8000/graphql` //`https://uodemand.holmes-dev.com/graphql`
    : `http://localhost:8000/graphql`;

const defaultOptions: DefaultOptions = {
  mutate: {
    fetchPolicy: "no-cache",
  },
};

const httpLink = createHttpLink({
  uri: uri,
});

export const client = new ApolloClient({
  link: httpLink,
  cache: new InMemoryCache(),
  defaultOptions: defaultOptions,
});
