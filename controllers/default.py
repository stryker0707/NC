# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################
import re
import os
import linecache
def index():
    form=FORM('Enter Noun Compound', INPUT(_name='name'), INPUT(_type='submit'))
    res=[]
    val=[]
    if form.process().accepted:
        a=form.vars.name
        a=a.split(' ')
        a=a[0]+'_NN '+a[1]+'_NN'
        rows = db(db.ncs.nc==a).select()
        if rows:
            sets = db(db.nnpp.nn==a).select()
            for row in rows:
                res.append(str(linecache.getline('../projects/paraphrase/pos_out/ukwac_out_1.txt', row.line)))
            if sets:
                for set in sets:
                    b=set.pp
                    k = db(db.pps.pp==b).select()
                    for j in k:
                        val.append(str(linecache.getline('../projects/paraphrase/pos_out/ukwac_out_1.txt', j.line)))
            else :
                val=['No Paraphrase occurences found']
        else:
            res = ["No such Noun compound Exists"]
            val=['No Paraphrase occurences found']
    print val, res
    return dict(form=form,res=res,val=val)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
