import React, {
} from 'react';

/**
 * Renders Sidebar as functional component
 * @param  {Object} props Topic to display
 * @return {ReactElement}
 */
const Sidebar = (props) => {
  const { topic } = props;
  if (topic === null) {
    return (
      <div className="wordcloud__container_sidebar">
        <div className="wordcloud__sidebar">
          <h1 className="wordcloud__sidebar_title">Information</h1>
          <p className="wordcloud__description">
            Choose a topic from the wordcloud to see some details.
          </p>
        </div>
      </div>
    );
  }
  return (
    <div className="wordcloud__container_sidebar">
      <div className="wordcloud__sidebar">
        <h1 className="wordcloud__sidebar_title">Information on topic "{topic.label}"</h1>
        <table className="wordcloud__sidebar_metatable">
          <thead>
          </thead>
          <tbody>
            <tr className="wordcloud__sidebar_metatable_row">
             <td className="wordcloud__sidebar_metatable_label">Total Mentions: </td>
             <td className="wordcloud__sidebar_metatable_value">{topic.volume || '0'}</td>
            </tr>
            <tr className="wordcloud__sidebar_metatable_row">
              <td className="wordcloud__sidebar_metatable_label">Positive Mentions: </td>
              <td className="wordcloud__sidebar_metatable_value wordcloud__sidebar_metatable_value--color-green">
                {topic.sentiment.positive || '0'}
              </td>
            </tr>
            <tr className="wordcloud__sidebar_metatable_row">
              <td className="wordcloud__sidebar_metatable_label">Neutral Mentions: </td>
              <td className="wordcloud__sidebar_metatable_value wordcloud__sidebar_metatable_value--color-grey">
                {topic.sentiment.neutral || '0'}
              </td>
           </tr>
            <tr className="wordcloud__sidebar_metatable_row">
              <td className="wordcloud__sidebar_metatable_label">Negative Mentions: </td>
              <td className="wordcloud__sidebar_metatable_value wordcloud__sidebar_metatable_value--color-red">
                {topic.sentiment.negative || '0'}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};


export default Sidebar;
