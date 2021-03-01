import React, { Component } from "react";
import { Button } from 'react-bootstrap';
import history from './../history';
import "./Employee.css";
import axios from "axios";
import ReactDOM from "react-dom";

 
export default class Employee extends Component {
  
  constructor(props) {
    super(props);
    this.state = {
      date:[],
      slots: [],
      appid:[],
      condate:[],
      conslots:[],
      conappid:[],
      appoid:""
    }
  
    this.baseState=this.state;
    this.getConfirmedApp = this.getConfirmedApp.bind(this);
    this.handleChange = this.handleChange.bind(this);
   
  }

  handleChange(event) {
    this.setState({
      [event.target.name]: event.target.value,
    });
  }


  componentDidMount() {
    
    axios.get('http://0.0.0.0:8001/carrierbyuserid/'+localStorage.getItem("userid"))
    .then(response => {
  // this.setState({carririd:response.data.id})
      axios.get('/appointments_carrier_NotConfirmed?carrier_id='+response.data.id)
      .then(response => {
        console.log(response.data);
        if(response.data.length != 0){
          var tableone="";
          response.data.forEach((element) => {
            const number = element.number;
            const date = element.dateofapp;
            const appid = element.id;
            this.setState((state) => {
              state.slots.push(number);
              state.date.push(date);
              state.appid.push(appid);
            });
          });
          console.log(this.state.slots+" --- "+this.state.date+"--"+this.state.appid)
          var s = '<div className="not-table"><table><tr><th>slot</th><th>date</th><th>id</th><th></th></tr>';
          console.log("skata");
          var i=0;
          this.state.slots.forEach((element) => {
            s +='<tr><td>'+ element +'</td>';
            s +='<td>'+ this.state.date[i] +'</td>';
            s +='<td id='+this.state.appid[i]+'>'+ this.state.appid[i] +'</td>';
            s +='</tr>'
            i++;
          }
          );
        //   jQuery('#appointbutton').click(function(e){
        //     console.log('a');
        // })
      
           s += '<tr></tr></table></div>';
           var view =(
            <div dangerouslySetInnerHTML={{ __html: s }} />
          );
          ReactDOM.render(view, document.getElementById("notconfirmed"));
        }
      })
      .catch(error => {
        console.log(error);
      });
      console.log(response.data);
    })
    .catch(error => {
      console.log(error);
    });


//For confirmed appontmntssssssss

     axios.get('http://0.0.0.0:8001/carrierbyuserid/'+localStorage.getItem("userid"))
    .then(response => {
  // this.setState({carririd:response.data.id})
      axios.get('/appointments_carrier_Confirmed?carrier_id='+response.data.id)
      .then(response => {
        console.log(response.data);
        if(response.data.length != 0){
          var tableone="";
          response.data.forEach((element) => {
            const number = element.number;
            const date = element.dateofapp;
            const appid = element.id;
            this.setState((state) => {
              state.conslots.push(number);
              state.condate.push(date);
              state.conappid.push(appid);
            });
          });
          console.log(this.state.slots+" --- "+this.state.date+"--"+this.state.appid)
          var s = '<div className="con-table"><table><tr><th>slot</th><th>date</th><th>id</th><th></th></tr>';
          console.log("skata");
          var i=0;
          this.state.conslots.forEach((element) => {
            s +='<tr><td>'+ element +'</td>';
            s +='<td>'+ this.state.condate[i] +'</td>';
            s +='<td id='+this.state.conappid[i]+'>'+ this.state.conappid[i] +'</td>';
            s +='</tr>'
            i++;
          }
          );
        //   jQuery('#appointbutton').click(function(e){
        //     console.log('a');
        // })
      
           s += '</table></div>';
           var view =(
            <div dangerouslySetInnerHTML={{ __html: s }} />
          );
          ReactDOM.render(view, document.getElementById("confirmed-table"));
        }
      })
      .catch(error => {
        console.log(error);
      });
      console.log(response.data);
    })
    .catch(error => {
      console.log(error);
    });

   

  }

  async getConfirmedApp() {

   

  }
  submitappointment(){
  console.log(this.state.appoid)
  axios({
    url: "/appointments_update/{id}?appointment_id="+this.state.appoid,
    method: "put",
    mode: "no-cors",
    headers: {
      common: {
        Accept: "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "Access-Control-Allow-Origin": "*",
      },
      "Access-Control-Allow-Origin": "*",
    },
    proxy: {
      host: "localhost",
      port: "5002",
    },
    
  })
    .then((response) => {
      console.log(response.statusText);
      console.log("data inserted to appointment--------------");
      console.log(this.state.slots+"old slots");
      refresh();
    })
    .catch(function (error) {
      console.log("data inserted to appointment--------------");
      console.log(error);
    });

  function refresh(){
    window.location.reload(false);
 
  }

  }
  render() {
    return (
      <div id="main">
        <h3>Appointments to be confirmed</h3>
        <div id="notconfirmed" className="not-conf"></div>
        <div id="btn">
        <input  
                  type="name"
                  name="appoid"
                  onChange={this.handleChange}
                  placeholder="id"
                />
       <button type="submit"  onClick={()=>{this.submitappointment()}}>Search</button>
       
       <h3 id="second">Confirmed Appointments</h3>

           <div id="confirmed-table">
           </div>
        </div>
      </div>
    );
  }
}