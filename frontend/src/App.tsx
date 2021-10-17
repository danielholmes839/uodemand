import React from "react";
import {
  BrowserRouter as Router,
  Redirect,
  Route,
  Switch,
} from "react-router-dom";

import { Workouts } from "components/Workouts";
import { Workout } from "components/Workout";

const App: React.FC = () => {
  return (
    <div className="container mx-auto px-3 mt-5">
      <h1 className="text-3xl">📈 uOttawa Gym Demand </h1>
      <Router>
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
