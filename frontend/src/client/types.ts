import { gql } from '@apollo/client';
import * as Apollo from '@apollo/client';
export type Maybe<T> = T | null;
export type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
export type MakeOptional<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]?: Maybe<T[SubKey]> };
export type MakeMaybe<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]: Maybe<T[SubKey]> };
const defaultOptions =  {}
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: string;
  String: string;
  Boolean: boolean;
  Int: number;
  Float: number;
  CURSOR: any;
  ISO8601: any;
};

export type PageInfo = {
  __typename?: 'PageInfo';
  endCursor: Scalars['CURSOR'];
  hasNextPage: Scalars['Boolean'];
  hasPreviousPage: Scalars['Boolean'];
  startCursor: Scalars['CURSOR'];
};

export type Query = {
  __typename?: 'Query';
  workout?: Maybe<Workout>;
  workoutGroup?: Maybe<WorkoutGroup>;
  workouts?: Maybe<WorkoutConnection>;
};


export type QueryWorkoutArgs = {
  id: Scalars['ID'];
};


export type QueryWorkoutGroupArgs = {
  barcode: Scalars['Int'];
};


export type QueryWorkoutsArgs = {
  after?: Maybe<Scalars['CURSOR']>;
  before?: Maybe<Scalars['CURSOR']>;
  first?: Maybe<Scalars['Int']>;
  last?: Maybe<Scalars['Int']>;
};

export type Workout = {
  __typename?: 'Workout';
  available: Scalars['Int'];
  barcode: Scalars['Int'];
  count: Scalars['Int'];
  duration: Scalars['Int'];
  group: WorkoutGroup;
  id: Scalars['ID'];
  location: Scalars['String'];
  time: Scalars['ISO8601'];
  timestamp: Scalars['ISO8601'];
  title: Scalars['String'];
};

export type WorkoutConnection = {
  __typename?: 'WorkoutConnection';
  edges: Array<WorkoutEdge>;
  pageInfo: PageInfo;
};

export type WorkoutEdge = {
  __typename?: 'WorkoutEdge';
  cursor: Scalars['CURSOR'];
  node: Workout;
};

export type WorkoutGroup = {
  __typename?: 'WorkoutGroup';
  first: Workout;
  last: Workout;
  workouts: Array<Workout>;
};

export type WorkoutsForwardQueryVariables = Exact<{
  first: Scalars['Int'];
  after?: Maybe<Scalars['CURSOR']>;
}>;


export type WorkoutsForwardQuery = { __typename?: 'Query', workouts?: { __typename?: 'WorkoutConnection', pageInfo: { __typename?: 'PageInfo', hasPreviousPage: boolean, hasNextPage: boolean, startCursor: any, endCursor: any }, edges: Array<{ __typename?: 'WorkoutEdge', cursor: any, node: { __typename?: 'Workout', id: string, barcode: number, title: string, location: string, available: number, duration: number, time: any, timestamp: any, count: number } }> } | null | undefined };


export const WorkoutsForwardDocument = gql`
    query WorkoutsForward($first: Int!, $after: CURSOR) {
  workouts(first: $first, after: $after) {
    pageInfo {
      hasPreviousPage
      hasNextPage
      startCursor
      endCursor
    }
    edges {
      cursor
      node {
        id
        barcode
        title
        location
        available
        duration
        time
        timestamp
        count
      }
    }
  }
}
    `;

/**
 * __useWorkoutsForwardQuery__
 *
 * To run a query within a React component, call `useWorkoutsForwardQuery` and pass it any options that fit your needs.
 * When your component renders, `useWorkoutsForwardQuery` returns an object from Apollo Client that contains loading, error, and data properties
 * you can use to render your UI.
 *
 * @param baseOptions options that will be passed into the query, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options;
 *
 * @example
 * const { data, loading, error } = useWorkoutsForwardQuery({
 *   variables: {
 *      first: // value for 'first'
 *      after: // value for 'after'
 *   },
 * });
 */
export function useWorkoutsForwardQuery(baseOptions: Apollo.QueryHookOptions<WorkoutsForwardQuery, WorkoutsForwardQueryVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useQuery<WorkoutsForwardQuery, WorkoutsForwardQueryVariables>(WorkoutsForwardDocument, options);
      }
export function useWorkoutsForwardLazyQuery(baseOptions?: Apollo.LazyQueryHookOptions<WorkoutsForwardQuery, WorkoutsForwardQueryVariables>) {
          const options = {...defaultOptions, ...baseOptions}
          return Apollo.useLazyQuery<WorkoutsForwardQuery, WorkoutsForwardQueryVariables>(WorkoutsForwardDocument, options);
        }
export type WorkoutsForwardQueryHookResult = ReturnType<typeof useWorkoutsForwardQuery>;
export type WorkoutsForwardLazyQueryHookResult = ReturnType<typeof useWorkoutsForwardLazyQuery>;
export type WorkoutsForwardQueryResult = Apollo.QueryResult<WorkoutsForwardQuery, WorkoutsForwardQueryVariables>;