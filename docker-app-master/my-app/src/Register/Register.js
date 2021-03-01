import React from "react";
import loginImg from "../login.svg";
import history from './../history';
import "./Register.css";
import axios from "axios";


export class Register extends React.Component {
  constructor(props) {
     super(props);
     this.state = {
       name:"",
       surname:"",
       role:"",
       email:"",
       dateofbirth:"",
       username: "",
       password: "",
      loginErrors: "",
    };
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
   // this.registerClick = this.registerClick.bind(this);
  }

  handleChange(event) {
    this.setState({
      [event.target.name]: event.target.value,
    });
  }

  handleSubmit(e) {
    const { username, password,name,surname,role,email,dateofbirth } = this.state;
    const data = { username, password,name,surname,role,email,dateofbirth };

    e.preventDefault();

    console.log(JSON.stringify(data));

    var formBody = new FormData();
    formBody.append("username", this.state.username);
    formBody.append("password", this.state.password);
    
      axios({
        url: "http://0.0.0.0:8001/users",
        method: "post",
        mode: "cors",
        headers: {
          common: {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
          },
          "Access-Control-Allow-Origin": "*"
        },
        data: JSON.stringify(data),
      }).then((response) => {
        console.log(response.statusText);
        if (response.status < 200 || response.status >= 300) {
          //throw new Error(response.statusText);
          console.log(response.json());
        } else {
        
          
          return response.json;
        }
      })
     
      .catch(function (error){
        console.log(error);
      });
    }

  render() {
    return (
      <form className="headform" onSubmit={this.handleSubmit}>
      <div className="base-container" ref={this.props.containerRef}>
        <div className="header">Register</div>
        <div className="content">
          <div className="image">
            <img src={loginImg} alt="" />
          </div>
          <div className="form">
          <div className="form-group">
              <label htmlFor="name">Name</label>
              <input type="text"  value={this.state.name}
                  onChange={this.handleChange} name="name" placeholder="name" />
            </div>
            <div className="form-group">
              <label htmlFor="surname">Surname</label>
              <input type="text"  value={this.state.surname}
                  onChange={this.handleChange} name="surname" placeholder="surname" />
            </div>
            <div className="form-group">
              <label htmlFor="username">Username</label>
              <input type="text"  value={this.state.username}
                  onChange={this.handleChange} name="username" placeholder="username" />
            </div>
            <div className="form-group">
              <label htmlFor="role">Role</label>
              <input type="text"  value={this.state.role}
                  onChange={this.handleChange} name="role" placeholder="role" />
            </div>
            <div className="form-group">
              <label htmlFor="dateofbirth">Birthd date</label>
              <input type="text"  value={this.state.dateofbirth}
                  onChange={this.handleChange} name="dateofbirth" placeholder="birthd date" />
            </div>
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input type="text"  value={this.state.email}
                  onChange={this.handleChange} name="email" placeholder="email" />
            </div>
            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input type="text"  value={this.state.password}
                  onChange={this.handleChange} name="password" placeholder="password" />
            </div>
          </div>
        </div>
        <div className="footer">
        <input type="submit" value="Submit" />
        </div>
      </div>
      </form>
    );
  }
}
export default Register;