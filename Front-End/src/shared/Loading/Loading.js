import React from 'react'
import gifLoading from "../../assets/img/loading.gif"
import "./Loading.scss"
export const Loading = () => {
    return (
        <div className="d-flex justify-content-center align-items-center Loading">
            <img src={gifLoading} alt=""></img>
        </div>
    )
}
