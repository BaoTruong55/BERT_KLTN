import _orderBy from 'lodash/orderBy';
import _map from 'lodash/map';

/**
 * Returns min and max volume as an object.
 * @param  {Object[]} topics Structured topics
 * @return {Object} Object with values minVolume and maxVolume
 */
export function getMinMaxVolume(topics) {
  /** Use orderBy. Just a single sort process needed **/
  const sortedTopics = _orderBy(topics, 'volume');

  return {
    minVolume: sortedTopics[0].volume,
    maxVolume: sortedTopics[sortedTopics.length - 1].volume,
  };
}


/**
 * Return fontSize
 * @param  {int} volume       Volume of certain element
 * @param  {int} maxVolume    maximum volume available
 * @param  {int} minVolume    minimum volume available
 * @param  {int[]} fontSizes  available font sizes
 * @return {int}              Element of provided fontSizes
 */
export function getFontSize(volume, maxVolume, minVolume, fontSizes) {
  const multiplier = (maxVolume - minVolume) / (fontSizes.length - 1);
  return fontSizes[Math.floor(volume / multiplier)];
}

/**
 * Single function to compose other reducer functions
 * @param  {Object[]} topics    topics Structured topics
 * @param  {Int[]} fontSizes    available font sizes
 * @return {Object[]}           Object with additional values. Topics itself as entities.
 */
export function enrichTopics(topics, fontSizes) {
  const minMaxVolume = getMinMaxVolume(topics);
  const topicsWithFontSize = _map(topics, (topic) => Object.assign(
    {},
    topic,
    { fontSize: getFontSize(topic.volume, minMaxVolume.maxVolume, minMaxVolume.minVolume, fontSizes) }
  ));

  return {
    minVolume: minMaxVolume.minVolume,
    maxVolume: minMaxVolume.maxVolume,
    entities: topicsWithFontSize,
  };
}
