import React, {
  Component,
} from 'react';

/**
 * Import styles
 */
import 'normalize.css';
import './WordCloud.css';

/**
 * Import Elements
 */
import Cloud from './Cloud';
import Sidebar from './Sidebar';

/**
 * Compose individual components
 */
export default class WordCloud extends Component {

  /**
   * Set initial state of component
   * @param  {Object} props Props of component
   * @return {void}
   */
  constructor(props) {
    super(props);
    this.state = {
      selectedTopic: null,
    };
    this.onSelectTopic = this.onSelectTopic.bind(this);
  }

  /**
   * Click handler
   * @param  {String} topic Whole topic object
   * @return {void}
   */
  onSelectTopic(topic) {
    this.setState({
      selectedTopic: topic,
    });
  }

  /**
   * Compose components
   * @return {ReactElement} [description]
   */
  render() {
    const {
      fontName,
      fontSizes,
      height,
      topics,
      width,
    } = this.props;

    if (topics.length === 0) {
      return (<span>No topics available.</span>);
    }

    return (
      <section className="wordcloud">
        <Cloud
          fontName={fontName}
          fontSizes={fontSizes}
          height={height}
          onSelectTopic={this.onSelectTopic}
          selectedTopic={this.state.selectedTopic}
          topics={topics}
          width={width}
        />
        <Sidebar
          topic={this.state.selectedTopic}
        />
      </section>
    );
  }
}

WordCloud.defaultProps = {
  fontName: 'Sans-Serif',
  fontSizes: [23, 26, 30, 46, 55, 69],
  height: 600,
  topics: [],
  width: 1000,
};
