# uOttawa Workout Session Demand Tracker

Web application that tracks the demand for workout sessions at uOttawa gym facilities.


## Data

The data for this application is stored in PostgreSQL and is backed up to S3 using parquet files. Registration data is scraped from [uOttawa's website](https://geegeereg.uottawa.ca/geegeereg/Activities/ActivitiesDetails.asp?aid=316) every 20 minutes. The data is stored in PostgreSQL in a single table with the following format:

| column name | column type | description |
| --- | --- | --- |
| id | int | Auto incrementing primary key
| barcode | int | Workout session id
| title | string | Workout session title "women only", "express", "staff only"
| location | string | Workout session facility "minto", "mont petit"
| timestamp | datetime | When this data point was recorded
| time | datetime | Workout session start time
| duration | int | Workout session duration in minutes
| available | int | The number of spaces left open

## GraphQL API

GraphQL Endpoint: https://uodemand.holmes-dev.com/graphql


```graphql
scalar ISO8601 # Date time string
scalar CURSOR  # Opaque pagination cursor

type Workout {
    id: ID!
    barcode: Int!
    title: String!
    location: String!
    available: Int!
    duration: Int!
    time: ISO8601!          # When the workout session starts
    timestamp: ISO8601!     # When the workout session data was recorded
    count: Int!
}

# Workouts with the same barcode
type WorkoutGroup {
    workouts: [Workout!]!
    first: Workout!
    last: Workout!
}

type Query {
    workouts(first: Int, after: CURSOR, last: Int, before: CURSOR): WorkoutConnection
    workout(id: ID!): Workout
    workoutGroup(barcode: Int!): WorkoutGroup
}

type PageInfo {
    hasPreviousPage: Boolean!
    hasNextPage: Boolean!
    startCursor: CURSOR!
    endCursor: CURSOR!
}

type WorkoutConnection {
    pageInfo: PageInfo!
    edges: [WorkoutEdge!]!
}

type WorkoutEdge {
    cursor: CURSOR!
    node: Workout!
}
```

```
docker run --name uottawa-db -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=uottawa-workouts -d -p 5432:5432 postgres
```
