import React, {
  Component,
} from 'react';

import {
  enrichTopics,
} from '../utils/dataprocessor';

import d3Cloud from 'd3-cloud';

/**
 * Render the cloud using D3. Not stateless, because async rendering of d3-cloud
 */
export default class Cloud extends Component {
  constructor(props) {
    super(props);
    this.state = {
      cloudDimensions: [],
      isProcessing: true,
    };
  }

  /**
   * Process data. Add range of volumes and fontSizes
   * @return {void} Will call setState
   */
  componentDidMount() {
    if (this.props.topics.length === 0) {
      return;
    }
    const {
      fontName,
      fontSizes,
      height,
      topics,
      width,
    } = this.props;

    /** Start calculation of cloud */
    d3Cloud()
      .size([width, height])
      .words(enrichTopics(topics, fontSizes).entities)
      .padding(10)
      .font(fontName)
      .text((d) => d.label)
      .fontSize((d) => d.fontSize)
      .random(() => 0.5)
      .rotate(() => 0)
      .on('end', (cloudDimensions) => { this.setState({ cloudDimensions, isProcessing: false }); })
      .start();
  }

  /**
   * Render cloud as svg
   * @return {ReactElement} [description]
   */
  render() {
    const {
      fontName,
      height,
      onSelectTopic,
      selectedTopic,
      topics,
      width,
    } = this.props;

    if (this.state.isProcessing) {
      return (
        <div className="wordcloud__container_cloud">
          <span >Loading...</span>
        </div>
      );
    }

    /**
     * Build class names to highlight the selected component
     * @param  {Object} item  Topic item
     * @return {String}       Class names
     */
    const getClassNames = (item) => {
      let classNames = 'wordcloud__cloud_label';

      if (item.sentimentScore > 60) {
        classNames += ' wordcloud__cloud_label--color-green';
      } else if (item.sentimentScore < 40) {
        classNames += ' wordcloud__cloud_label--color-red';
      } else {
        classNames += ' wordcloud__cloud_label--color-grey';
      }

      if (
        selectedTopic !== null
        && selectedTopic.hasOwnProperty('id')
        && selectedTopic.id === item.id
      ) {
        classNames += ' wordcloud__cloud_label--is-active';
      }
      return classNames;
    };

    return (
      <div className="wordcloud__container_cloud">
        <div className="wordcloud__cloud">
          <svg width={width} height={height}>
            <g transform={`translate(${width / 2}, ${height / 2})`}>
              {this.state.cloudDimensions.map(item =>
                <text
                  className={getClassNames(item)}
                  key={item.id}
                  onClick={() => onSelectTopic(item)}
                  style={{
                    fontSize: item.size,
                    fontFamily: fontName,
                  }}
                  textAnchor="middle"
                  transform={`translate(${item.x} , ${item.y} )`}
                >{item.text}</text>
              )}
            </g>
          </svg>
        </div>
        {topics.length > this.state.cloudDimensions.length ? <p className="worcloud__hint">Some topics cannot be displayed, because of the available space.</p> : ''}
      </div>
    );
  }
}

