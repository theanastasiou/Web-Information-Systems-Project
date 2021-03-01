import React, { Component } from "react";
import { Card, ListGroup } from "react-bootstrap";
import loginImg from "../login.svg";
import "./login.css";
import history from "./../history";
import axios from "axios";
import jwt_decode from 'jwt-decode';

export class login extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      username: "",
      password: "",
      loginErrors: "",
    };

    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.registerClick = this.registerClick.bind(this);
  }

  test() {
    fetch("/movies").then((response) =>
      response.json().then((data) => {
        console.log(data);
      })
    );
    //console.log("login clicked")
  }
  handleChange(event) {
    this.setState({
      [event.target.name]: event.target.value,
    });
  }

  handleSubmit(e) {
    const { username, password } = this.state;
    const data = { username, password };

    e.preventDefault();

    console.log(data);

    var formBody = new FormData();
    formBody.append("username", this.state.username);
    formBody.append("password", this.state.password);
    
      axios({
        url: "http://0.0.0.0:8000/auth/token",
        method: "post",
        mode: "cors",
        headers: {
          Accept: "application/json",
          "Access-Control-Allow-Origin": "*",
          "Content-type": "application/x-www-form-urlencoded",
        },
        data: formBody,
      }).then((response) => {
        console.log(response.statusText);
        if (response.status < 200 || response.status >= 300) {
          //throw new Error(response.statusText);
          console.log(response.detail);
        } else {
          
          const token = response.data.access_token;
          localStorage.setItem('token',token);
          localStorage.getItem('token');
          const decodedHeader = jwt_decode(token, {header: true});
          console.log(response);
          localStorage.setItem('mail',username);
          localStorage.setItem('userid',response.data.userid);
          localStorage.setItem('role',response.data.role);
          if(localStorage.getItem('role') == 0){
            this.props.history.push("/client");
          }else{
            this.props.history.push("/employee");
          }
          return response.json;
        }
      })
     
      .catch(function (error){
        console.log(error);
      });

      //   .then((res) => console.log(res));
   
  }

  // this.props.loginUser(userData);
  // const form = e.target;
  // const data = new FormData(form);

  registerClick(e) {
    e.preventDefault();
    this.props.history.push("/register");
  }

  render() {
    return (
      <form className="headform" onSubmit={this.handleSubmit}>
        <div className="base-container" ref={this.props.containerRef}>
          <div className="header">Login</div>
          <div className="content">
            <div className="image">
              <img src={loginImg} alt="login img" />
            </div>
            <div className="form">
              <div className="form-group">
                <label htmlFor="username">Username </label>
                <input
                  type="text"
                  value={this.state.username}
                  onChange={this.handleChange}
                  name="username"
                  placeholder="username"
                />
              </div>
              <div className="form-group">
                <label htmlFor="password">Password </label>
                <input
                  type="password"
                  name="password"
                  onChange={this.handleChange}
                  placeholder="password"
                />
              </div>
            </div>
          </div>
          <div className="footer">
            <input type="submit" value="Submit" />
          </div>
          <div calssName="footerR">
            <a href="/register" onClick={this.registerClick}>
              Not registered? Register here
            </a>
          </div>
        </div>
      </form>
    );
  }
}

export default login;
