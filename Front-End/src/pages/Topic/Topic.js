import React, { useEffect, useState } from 'react';
import './Topic.scss';
import WordCloud from './components/WordCloud';
// import axios from 'axios';

export const Topic = () => {
  // const [topics, setTopics] = useState();
  // const [isFetching, setIsFetching] = useState(true);
  const topic = {
    topics: [
      {
        id: '1751295897__Berlin',
        label: 'Berlin',
        volume: 165,
        type: 'topic',
        sentiment: {
          negative: 3,
          neutral: 133,
          positive: 29,
        },
        sentimentScore: 65,
               
      },
      {
        id: '1751295897__DJ',
        label: 'DJ',
        volume: 48,
        type: 'topic',
        sentiment: {
          neutral: 46,
          positive: 2,
        },
        sentimentScore: 54,
               
      },
      {
        id: '1751295897__Ostgut Ton',
        label: 'Ostgut Ton',
        volume: 24,
        type: 'topic',
        sentiment: {
          neutral: 22,
          positive: 2,
        },
        sentimentScore: 58,
               
      },
      {
        id: '1751295897__Hammered',
        label: 'Hammered',
        volume: 48,
        type: 'topic',
        sentiment: {
          neutral: 18,
          negative: 30,
        },
        sentimentScore: 20,
              
      },
      {
        id: '1751295897__Code',
        label: 'Code',
        volume: 16,
        type: 'topic',
        sentiment: {
          neutral: 13,
          positive: 3,
        },
        sentimentScore: 68,
               
      },
      {
        id: '1751295897__Quantified Drunk',
        label: 'Quantified Drunk',
        volume: 14,
        type: 'topic',
        sentiment: {
          neutral: 14,
        },
        sentimentScore: 50,
              
      },
      {
        id: '1751295897__Berghain resident',
        label: 'Berghain resident',
        volume: 13,
        type: 'topic',
        sentiment: {
          neutral: 10,
          positive: 3,
        },
        sentimentScore: 73,
              
      },
      {
        id: "1751295897__San Soda's Panorama Bar",
        label: "San Soda's Panorama Bar",
        volume: 13,
        type: 'topic',
        sentiment: {
          neutral: 13,
        },
        sentimentScore: 50,
               
      },
      {
        id: '1751295897__Germany',
        label: 'Germany',
        volume: 13,
        type: 'topic',
        sentiment: {
          neutral: 9,
          positive: 4,
        },
        sentimentScore: 80,
              
      },
      {
        id: '1751295897__Amsterdam',
        label: 'Amsterdam',
        volume: 12,
        type: 'topic',
        sentiment: {
          neutral: 7,
          positive: 5,
        },
        sentimentScore: 91,
               
      },
      {
        id: '1751295897__Kantine am Berghain',
        label: 'Kantine am Berghain',
        volume: 11,
        type: 'topic',
        sentiment: {
          neutral: 10,
          positive: 1,
        },
        sentimentScore: 59,
               
      },
      {
        id: '1751295897__London',
        label: 'London',
        volume: 11,
        type: 'topic',
        sentiment: {
          neutral: 8,
          positive: 3,
        },
        sentimentScore: 77,
              
      },
      {
        id: '1751295897__UK',
        label: 'UK',
        volume: 8,
        type: 'topic',
        sentiment: {
          neutral: 8,
        },
        sentimentScore: 50,
               
      },
      {
        id: '1751295897__Marcel Dettmann',
        label: 'Marcel Dettmann',
        volume: 8,
        type: 'topic',
        sentiment: {
          neutral: 5,
          positive: 3,
        },
        sentimentScore: 87,
               
      },
      {
        id: '1751295897__Disco',
        label: 'Disco',
        volume: 8,
        type: 'topic',
        sentiment: {
          neutral: 8,
        },
        sentimentScore: 50,
               
      },
      {
        id: '1751295897__Barcelona',
        label: 'Barcelona',
        volume: 7,
        type: 'topic',
        sentiment: {
          neutral: 7,
        },
        sentimentScore: 50,
              
      },
      {
        id: '1751295897__Watergate',
        label: 'Watergate',
        volume: 7,
        type: 'topic',
        sentiment: {
          neutral: 6,
          positive: 1,
        },
        sentimentScore: 64,
               
      },
      {
        id: '1751295897__debut LP',
        label: 'debut LP',
        volume: 6,
        type: 'topic',
        sentiment: {
          neutral: 3,
          positive: 3,
        },
        sentimentScore: 100,
               
      },
      {
        id: '1751295897__Patrick Gräser',
        label: 'Patrick Gräser',
        volume: 6,
        type: 'topic',
        sentiment: {
          neutral: 3,
          positive: 3,
        },
        sentimentScore: 100,
              
      },
      {
        id: '1751295897__Panorama Bar in Berlin',
        label: 'Panorama Bar in Berlin',
        volume: 6,
        type: 'topic',
        sentiment: {
          neutral: 4,
          positive: 2,
        },
        sentimentScore: 83,
               
      },
      {
        id: '1751295897__legendary nightclub',
        label: 'legendary nightclub',
        volume: 6,
        type: 'topic',
        sentiment: {
          positive: 6,
        },
        sentimentScore: 150,
              
      },
      {
        id: '1751295897__Ben Klock',
        label: 'Ben Klock',
        volume: 5,
        type: 'topic',
        sentiment: {
          neutral: 5,
        },
        sentimentScore: 50,
               
      },
      {
        id: '1751295897__Mixes',
        label: 'Mixes',
        volume: 5,
        type: 'topic',
        sentiment: {
          neutral: 5,
        },
        sentimentScore: 50,
               
      },
      {
        id: '1751295897__Panorama Bar Music',
        label: 'Panorama Bar Music',
        volume: 5,
        type: 'topic',
        sentiment: {
          neutral: 5,
        },
        sentimentScore: 50,
              
      },
      {
        id: '1751295897__Terrace Sundae',
        label: 'Terrace Sundae',
        volume: 5,
        type: 'topic',
        sentiment: {
          neutral: 5,
        },
        sentimentScore: 50,
              
      },
      {
        id: '1751295897__Jun',
        label: 'Jun',
        volume: 5,
        type: 'topic',
        sentiment: {
          neutral: 5,
        },
        sentimentScore: 50,
              
      },
      {
        id: '1751295897__Live set',
        label: 'Live set',
        volume: 4,
        type: 'topic',
        sentiment: {
          neutral: 3,
          positive: 1,
        },
        sentimentScore: 75,
               
      },
      {
        id: '1751295897__dance music',
        label: 'dance music',
        volume: 4,
        type: 'topic',
        sentiment: {
          neutral: 4,
        },
        sentimentScore: 50,
              
      },
      {
        id: '1751295897__club culture',
        label: 'club culture',
        volume: 3,
        type: 'topic',
        sentiment: {
          neutral: 3,
        },
        sentimentScore: 50,
              
      },
      {
        id: '1751295897__D/B Presents',
        label: 'D/B Presents',
        volume: 3,
        type: 'topic',
        sentiment: {
          neutral: 3,
        },
        sentimentScore: 50,
               
      },
    ],
  };

  return (
    <div className="row">
      <WordCloud topics={topic.topics} />
    </div>
  );
};
