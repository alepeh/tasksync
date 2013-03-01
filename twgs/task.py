""" Tasks. """
import abc

class DownstreamTask(object):
    """ Identifies this instance is a data sync. """

    @abc.abstractproperty
    def association(self):
        """ Get the unique association identifier for this task. """
        raise NotImplementedError

    @abc.abstractmethod
    def is_associated_with(self, upstream):
        """ Identify if this task is associated with an upstream task. """
        raise NotImplementedError

    @abc.abstractmethod
    def associate_with(self, upstream):
        """ Associate this task with an upstream task. """
        raise NotImplementedError

class UpstreamTask(object):
    """
    Identifies this instance may be associated with other resources. The
    actual association values should be globally unique an should
    withstand long-term retention.
    """

    @abc.abstractproperty
    def uid(self):
        """ Gets a unique association UID for this instance. """
        raise NotImplementedError

    @abc.abstractproperty
    def provider(self):
        """ Get a unique association name for this instance. """
        raise NotImplementedError

    @abc.abstractproperty
    def etag(self):
        """
        Return a unique identifier for the current state.
        """
        raise NotImplementedError

class Task(object):
    #pylint: disable=E0202
    """ An abstract task representation. """

    def __str__(self):
        return '%s[id=%s,p=%s,s=%s]' % (
                self.__class__.__name__, self.uid,
                self.project, self.subject)

    @abc.abstractproperty
    def uid(self):
        """
        Gets this task's unique identifier. This value may be used for
        long-term storage.
        """
        raise NotImplementedError

    @abc.abstractproperty
    def status(self):
        """ Return this task's status. """
        raise NotImplementedError

    @abc.abstractproperty
    def project(self):
        """ Return this task's project name. """
        raise NotImplementedError

    @abc.abstractproperty
    def subject(self):
        """
        Return this task's subject/title.
        """
        raise NotImplementedError

    @abc.abstractproperty
    def due(self):
        """
        Return a date object, or None, of the task's due date.
        """
        raise NotImplementedError

    @abc.abstractproperty
    def completed(self):
        """
        Return a date object, or None, of the task's time of completion.
        """
        raise NotImplementedError


    @property
    def is_completed(self):
        return self.status == 'completed'

    @property
    def is_pending(self):
        return self.status == 'pending'

    @property
    def is_deleted(self):
        return self.status == 'deleted'

    @property
    def should_sync(self):
        raise NotImplementedError

    @abc.abstractmethod
    def copy_from(self, other):
        raise NotImplementedError

    def __eq__(self, other):
        if other is None:
            return False

        return (self.subject == other.subject
            and self.project == other.project
            and self.due == other.due
            and self.completed == other.completed)

    def _set_or_delete(self, key, value, fmt=None):
        if value is None:
            if key in self._source:
                del self._source[key]
        else:
            if not fmt is None:
                value = fmt(value)
            self._source[key] = value

class TaskFactory(object):
    def create_from(self, **kwargs):
        """ Create a new task. """
        raise NotImplementedError

class TaskRepository(object):
    def all(self):
        """ Load all tasks. """
        raise NotImplementedError

    def save(self, task, batch=None, userdata=None, cb=None):
        """ Save the specified task. """
        raise NotImplementedError

    def delete(self, task, batch=None, userdata=None, cb=None):
        """ Delete the specified task. """
        raise NotImplementedError