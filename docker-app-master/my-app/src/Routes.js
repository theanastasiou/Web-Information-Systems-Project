import React, { Component } from "react";
import { Router, Switch, Route } from "react-router-dom";

import About from "./About/About";
import Contact from "./Contact/Contact";
import Products from "./Product/Products";
import Home from "./Home/Home";
import ClientPage from "./ClientPage/Client";
import EmployeePage from "./EmployeePage/Employee";
import login from "./Login/login";
import history from './history';
import { Register } from "./Register/Register";


export default class Routes extends Component {
    render() {
        return (
            <Router history={history}>
                <Switch>
                    <Route path="/" exact component={Home} />
                    <Route path="/About" component={About} />
                    <Route path="/Contact" component={Contact} />
                    <Route path="/Products" component={Products} />
                    <Route path="/login" component={login} />
                    <Route path="/client" component={ClientPage} />
                    <Route path="/employee" component={EmployeePage} />
                    <Route path="/register" component={Register} />
                </Switch>
            </Router>
        )
    }
}
