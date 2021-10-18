import React from "react";
import {
  BrowserRouter as Router,
  Redirect,
  Route,
  Switch,
  NavLink,
} from "react-router-dom";

import { Workouts } from "components/Workouts";
import { Workout } from "components/Workout";

const App: React.FC = () => {
  return (
    <div className="container mx-auto px-3 mt-5">
      <Router>
        <h1 className="text-3xl">
          📈 uOttawa Demand
          <NavLink
            className="text-base text-gray-600 bg-gray-50 hover:bg-gray-100 px-5 p-1 mt-1 rounded font-semibold float-right"
            activeClassName="hidden"
            to="/workouts?view=future"
          >
            Workouts
          </NavLink>
        </h1>

        <p className="text-sm mt-3">
          Website that tracks the demand for workout sessions at uOttawa's gym
          facilities.
        </p>
        <Switch>
          <Route path="/workouts" exact>
            <Workouts />
          </Route>
          <Route path="/workout/:barcode" exact>
            <Workout />
          </Route>
          <Route path="/">
            <Redirect to="/workouts" />
          </Route>
        </Switch>
      </Router>
    </div>
  );
};

export default App;
