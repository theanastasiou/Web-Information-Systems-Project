import React, { Component } from "react";
import { Button } from 'react-bootstrap';
import history from './../history';

import "./Home.css";

export default class Home extends Component {
  render() {
    return (
      <div className="Home">
        <div className="lander">
          <h1>Welcome to EMR Apointment Service</h1>
          <p>Login an make your apointment to your nearest spot.</p>
        
          <div className="lastbtn">
          <Button variant="btn btn-success" onClick={() => history.push('/login')}>Login/Register</Button>
          </div>
        </div>
      </div>
    );
  }
}
