'''
      _               _ _
   __| |_      _____ | | | __ _
  / _` \ \ /\ / / _ \| | |/ _` |
 | (_| |\ V  V / (_) | | | (_| |
  \__,_| \_/\_/ \___/|_|_|\__,_|

  An official requests based wrapper for the Dwolla API.

  This file contains functionality for all requests related endpoints.
'''

from . import constants as c
from .rest import r


def create(sourceid, amount, **kwargs):
    """
    Requests money from a user for a user associated with
    the current OAuth token.

    :param sourceid: String with Dwolla ID to request funds from.
    :param amount: Double with amount to request.
    :param params: Dictionary with additional parameters.

    :**kwargs: Additional parameters for API or client control. 
    If a "params" key with Dictionary value is passed all other 
    params in **kwargs will be discarded and only the values 
    in params used.

    :return: Integer with Request ID of submitted request.
    """
    if not sourceid:
        raise Exception('create() requires sourceid parameter')
    if not amount:
        raise Exception('create() requires amount parameter')

    p = {
        'oauth_token': kwargs.pop('alternate_token', c.access_token),
        'sourceId': sourceid,
        'amount': amount
    }

    if 'params' in kwargs:
        p = dict(list(p.items()) + list(kwargs['params'].items()))
    elif kwargs:
        p = dict(list(p.items()) + list(kwargs.items()))

    return r._post('/requests/', p, dwollaparse=p.pop('dwollaparse', 'dwolla'))


def get(**kwargs):
    """
    Retrieves a list of pending money requests for the user
    associated with the current OAuth token.

    :param params: Dictionary with additional parameters.

    :**kwargs: Additional parameters for API or client control. 
    If a "params" key with Dictionary value is passed all other 
    params in **kwargs will be discarded and only the values 
    in params used.

    :return: Dictionary with pending money requests and relevant data.
    """
    p = {'oauth_token': kwargs.pop('alternate_token', c.access_token)}

    if 'params' in kwargs:
        p = dict(list(p.items()) + list(kwargs['params'].items()))
    elif kwargs:
        p = dict(list(p.items()) + list(kwargs.items()))

    return r._get('/requests', p, dwollaparse=p.pop('dwollaparse', 'dwolla'))


def info(requestid, **kwargs):
    """
    Retrieves additional information about a pending money
    request.

    :param requestid: String with Request ID to retrieve info for.

    :param kwargs: Additional parameters for client control.

    :return: Dictionary with information relevant to the request.
    """
    if not requestid:
        raise Exception('info() requires requestid parameter')

    return r._get('/requests/' + requestid, 
                    {
                        'oauth_token': kwargs.pop('alternate_token', c.access_token)
                    }, dwollaparse=kwargs.pop('dwollaparse', 'dwolla'))


def cancel(requestid, **kwargs):
    """
    Cancels a pending money request.

    :param requestid: String with Request ID to cancel.

    :param kwargs: Additional parameters for client control.
    
    :return: None
    """
    if not requestid:
        raise Exception('cancel() requires requestid parameter')

    return r._post('/requests/' + requestid + '/cancel/', 
                    {
                        'oauth_token': kwargs.pop('alternate_token', c.access_token)
                    }, dwollaparse=kwargs.pop('dwollaparse', 'dwolla'))


def fulfill(requestid, amount, **kwargs):
    """
    Fulfills a pending money request.

    :param requestid: String with Request ID to fulfill.
    :param amount: Double with amount to fulfill.
    :param params: Dictionary with additional parameters.

    :**kwargs: Additional parameters for API or client control. 
    If a "params" key with Dictionary value is passed all other 
    params in **kwargs will be discarded and only the values 
    in params used.

    :return: Dictionary with information (transaction/request IDs) relevant to fulfilled request.
    """
    if not requestid:
        raise Exception('fulfill() requires requestid parameter')
    if not amount:
        raise Exception('fulfill() requires amount parameter')

    p = {'oauth_token': kwargs.pop('alternate_token', c.access_token),
         'amount': amount,
         'pin': kwargs.pop('alternate_pin', c.pin)}

    if 'params' in kwargs:
        p = dict(list(p.items()) + list(kwargs['params'].items()))
    elif kwargs:
        p = dict(list(p.items()) + list(kwargs.items()))

    return r._post('/requests/' + requestid + '/fulfill', p, dwollaparse=p.pop('dwollaparse', 'dwolla'))