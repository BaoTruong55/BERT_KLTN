import React from 'react';

export const PostDetail = (props) => {
  return (
    <div className="row m-0 pb-2 mb-4 border-bottom">
      <div className="col-md-8">
        <a
          href={props.link}
          target="_blank"
          className="link-style"
          rel="noopener noreferrer"
        >
          <h3>{props.title}</h3>
        </a>
        <p>{props.description}</p>
      </div>
      <div className="col-md-4 thumb-art">
        <img src={props.thumbnailUrl} className="thumb-art_img" alt="" />
      </div>
    </div>
  );
};
