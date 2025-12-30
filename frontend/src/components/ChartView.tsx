/** 图表展示组件 */
import React from 'react';

interface ChartViewProps {
  type: string;
  data: string; // base64 encoded image
}

const ChartView: React.FC<ChartViewProps> = ({ type, data }) => {
  if (!data) {
    return <div>无图表数据</div>;
  }

  return (
    <div style={{ textAlign: 'center', padding: '16px' }}>
      <img
        src={`data:image/png;base64,${data}`}
        alt={`${type}图表`}
        style={{
          maxWidth: '100%',
          height: 'auto',
          border: '1px solid #d9d9d9',
          borderRadius: '4px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        }}
      />
      <div style={{ marginTop: 8, fontSize: 12, color: '#666' }}>
        图表类型: {type.toUpperCase()}
      </div>
    </div>
  );
};

export default ChartView;
