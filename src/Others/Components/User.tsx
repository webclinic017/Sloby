import React, {useContext} from "react"
import { Link, Outlet } from "react-router-dom"
import {UserContext} from "../Context/UserContext"
function Profile() {
    const {
        first_name,
        set_first_name,
        last_name,
        set_last_name,
        country,
        set_country,
        email,
        set_email,
        user_name,
        set_user_name,
        phone_number,
        set_phone_number
    } = useContext<any>(UserContext)
  return (
    <div className="profile-container content-base">
        <h1 className="title-base">Profile</h1>

        <hr/>
        <div className="profile-information">
              <div className="name-container">
            <input className="input-base" type="text" placeholder="First ame"/>
            <input className="input-base" type="text" placeholder="Last name"/>
            </div>
        <div className="other-information">
            <input className="input-base" type="text" placeholder="Country"/>
            <input className="input-base" type="text" placeholder="Email"/>
            <input className="input-base" type="text" placeholder="User Name"/>
            <input className="input-base" type="text" placeholder="Phone number"/>
        </div>
        </div>

    </div>
  )
}

export default Profile;
