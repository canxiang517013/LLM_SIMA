/** 消息列表组件 */
import React from 'react';
import { List, Typography, Tag, Card } from 'antd';
import { UserOutlined, RobotOutlined } from '@ant-design/icons';
import { Message } from '../types';
import ChartView from './ChartView';

const { Paragraph, Text } = Typography;

interface MessageListProps {
  messages: Message[];
}

const MessageList: React.FC<MessageListProps> = ({ messages }) => {
  return (
    <List
      dataSource={messages}
      renderItem={(message) => (
        <List.Item key={message.id} style={{ border: 'none', padding: '12px 0' }}>
          <div
            style={{
              width: '100%',
              display: 'flex',
              justifyContent: message.role === 'user' ? 'flex-end' : 'flex-start',
            }}
          >
            <Card
              style={{
                maxWidth: '80%',
                backgroundColor: message.role === 'user' ? '#e6f7ff' : '#f5f5f5',
                border: message.role === 'user' ? '1px solid #91d5ff' : '1px solid #d9d9d9',
              }}
            >
              <div style={{ marginBottom: 8 }}>
                {message.role === 'user' ? (
                  <Tag icon={<UserOutlined />} color="blue">
                    用户
                  </Tag>
                ) : (
                  <Tag icon={<RobotOutlined />} color="green">
                    助手
                  </Tag>
                )}
                <Text type="secondary" style={{ marginLeft: 8, fontSize: 12 }}>
                  {new Date(message.timestamp).toLocaleTimeString()}
                </Text>
              </div>
              
              <Paragraph style={{ marginBottom: 12, whiteSpace: 'pre-wrap' }}>
                {message.content}
              </Paragraph>
              
              {/* 显示表格数据 */}
              {(message.dataType === 'table' || message.dataType === 'table_and_chart') && message.data?.table && (
                <div style={{ marginTop: 16 }}>
                  <Text strong>查询结果：</Text>
                  <div style={{ marginTop: 8, overflowX: 'auto' }}>
                    <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 12 }}>
                      <thead>
                        <tr style={{ backgroundColor: '#fafafa' }}>
                          {Object.keys(message.data.table[0] || {}).map((key) => (
                            <th
                              key={key}
                              style={{
                                padding: '8px 12px',
                                border: '1px solid #d9d9d9',
                                textAlign: 'left',
                                fontWeight: 600,
                              }}
                            >
                              {key}
                            </th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {message.data.table.map((row: any, index: number) => (
                          <tr key={index}>
                            {Object.values(row).map((value: any, cellIndex: number) => (
                              <td
                                key={cellIndex}
                                style={{
                                  padding: '8px 12px',
                                  border: '1px solid #d9d9d9',
                                }}
                              >
                                {String(value)}
                              </td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
              
              {/* 显示图表 */}
              {(message.dataType === 'chart' || message.dataType === 'table_and_chart') && message.data?.chart && (
                <div style={{ marginTop: 16 }}>
                  <ChartView
                    type={message.data.chart.type}
                    data={message.data.chart.data}
                  />
                </div>
              )}
            </Card>
          </div>
        </List.Item>
      )}
    />
  );
};

export default MessageList;
