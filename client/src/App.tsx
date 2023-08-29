import React from 'react';
import logo from './logo.svg';
import './App.css';

import { Container, Col, Row } from 'react-bootstrap';

function App() {
  return (
    <Container>
      <Row className="text-center">
        <Col>Bootstrap</Col>
        <Col>React</Col>
      </Row>

      <Row className="text-center">
        <Col>Hello!</Col>
      </Row>
    </Container>
  );
}

export default App;
