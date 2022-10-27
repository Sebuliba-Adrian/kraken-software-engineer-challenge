import unittest
from api import app, db
from api import Application


class ApplicationModelCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
        db.create_all()

        self.alpha = Application(
            name="alpha",
            version="1.2.0",
            stack="python-django",
            description="This application provides alpha services.",
            team="Unicorn",
            owner="john.doe@tradebyte.com",
            eks_size="xl",
        )
        self.beta = Application(
            name="beta",
            version="1.0.0",
            stack="java-spring",
            description="This application provides beta services on top of alpha.",
            team="“Duck”",
            owner="max.mustermann@tradebyte.com",
            eks_size="m",
        )
        db.session.add(self.alpha)
        db.session.add(self.beta)
        db.session.commit()

    def tearDown(self):
        db.session.close()
        db.drop_all()
        self.app_context.pop()

    def test_no_duplicate_dependencies_can_be_added(self):
        self.beta.add_dependent_app(self.alpha)
        self.beta.add_dependent_app(self.alpha)
        db.session.commit()
        self.assertEqual(self.beta.get_child, 1)

    def test_removal_of_dependency_removes_association(self):
        self.beta.remove_dependent_app(self.alpha)
        db.session.commit()
        self.assertFalse(self.alpha.is_dependency_of(self.beta))

    def test_dependency_can_be_established_between_apps(self):

        self.assertEqual(self.alpha.depends_on, [])
        self.assertEqual(self.beta.depends_on, [])

        self.beta.add_dependent_app(self.alpha)
        db.session.commit()
        self.assertTrue(self.alpha.is_dependency_of(self.beta))
        self.assertFalse(self.beta.is_dependency_of(self.alpha))

        self.assertEqual(self.alpha.depends_on, [])
        self.assertEqual(self.beta.depends_on, [self.alpha])


if __name__ == "__main__":
    unittest.main(verbosity=2)
