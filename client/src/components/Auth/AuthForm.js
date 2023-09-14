import React from 'react';
import { Form, useActionData, useNavigation } from 'react-router-dom';

import FloatingLabel from 'react-bootstrap/FloatingLabel';
import { Form as BootForm } from 'react-bootstrap';
import Button from 'react-bootstrap/Button';

import './AuthForm.css';

const AuthForm = () => {
  const data = useActionData();

  const authFailed = data && data.code === 401;

  const navigation = useNavigation();

  const isSubmitting = navigation.state === 'submitting';

  return (
    <div className="signin-body d-flex align-items-center py-4 bg-body-tertiary">
      <main className="form-signin w-100 m-auto">
        <Form method="POST">
          <h1 className="h3 mb-3 fw-normal">Client</h1>

          <FloatingLabel controlId="emailInput" label="Email">
            <BootForm.Control
              className="form-control"
              name="email"
              type="email"
              placeholder="email@exaple.com"
              required
            />
          </FloatingLabel>

          <FloatingLabel controlId="passwordInput" label="Password">
            <BootForm.Control
              className="form-control"
              name="password"
              type="password"
              placeholder="password"
              required
            />
          </FloatingLabel>

          <BootForm.Group className="mb-3" controlId="rememberMeInput">
            <BootForm.Check type="checkbox" label="Remember me" />
          </BootForm.Group>
          {authFailed && <p style={{ color: 'red' }}>Invalid credentials!</p>}
          <Button
            variant="primary"
            type="submit"
            className="btn btn-primary w-100 py-2"
            disabled={isSubmitting}
          >
            {isSubmitting ? 'Loading...' : 'Sign in'}
          </Button>
        </Form>
      </main>
    </div>
  );
};

export default AuthForm;
