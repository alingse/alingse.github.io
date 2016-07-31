#!/usr/bin/env python
#coding=utf-8
#author@alingse
#2016.07.30

from __future__ import print_function
from operator import itemgetter

import argparse
import shutil
import yaml
import os


__path__source = '_source'
__path__template = '_template'
__path_article = 'article'



def find_buildhome(cur_dir=None):
    if cur_dir == None:
        cur_dir = os.path.dirname(os.path.abspath(__file__))
    else:
        cur_dir = cur_dir.rstrip('/')

    buildhome = None
    while buildhome == None and cur_dir != '':
        if '.git' in os.listdir(cur_dir):
            buildhome = cur_dir
            #return buildhome
            break
        cur_dir = cur_dir[:cur_dir.rfind('/')]
    return buildhome


def load_yaml_meta(htmlpath):
    fname = os.path.basename(htmlpath)
    fid = int(fname.split('.',1)[0])
    f = open(htmlpath,'r')
    html = f.read().decode('utf-8')

    sk = html.find('<YAML-META-INFO-START/>')
    ek = html.find('<YAML-META-INFO-END/>')
    if sk == -1 or ek == -1:
        return False,htmlpath
    tmp = html[sk:ek]
    sk = tmp.find('<!--')
    ek = tmp.rfind('-->')
    if sk == -1 or ek == -1:
        return False,htmlpath
    meta = tmp[sk+4:ek]
    meta = yaml.load(meta)
    meta['fid'] = fid
    return True,meta


def load_source_metas(buildhome):
    source_path = os.path.join(buildhome,__path__source)

    error_metas = []
    metas = []
    for fname in os.listdir(source_path):
        htmlpath = os.path.join(source_path,fname)
        if htmlpath.endswith('.html'):
            status,meta = load_yaml_meta(htmlpath)
            meta['htmlpath'] = htmlpath
            if status:
                metas.append(meta)
            else:
                error_metas.append(meta)

    return metas,error_metas


def aggregate_metas(metas):
    #if id is error
    def id_conflict(metas):
        bad_ids = set()
        bad_metas = []
        exit = False
        while not exit:
            exit = True
            _metas = []
            for meta in metas:
                fid = meta['fid']
                id = meta['id']
                if fid != id or fid in bad_ids or id in bad_ids:
                    bad_ids.add(fid)
                    bad_ids.add(id)
                    bad_metas.append(meta)
                    exit = False
                else:
                    _metas.append(meta)
            metas = _metas

        return bad_metas,metas

    def cat_aggregate(metas):
        cats = {}
        for meta in metas:
            _cat = meta['cat']
            if _cat not in cats:
                cats[_cat] = {'name':_cat,'metas':[]}
            cats[_cat]['metas'].append(meta)

        return cats

    def tag_aggregate(metas):
        tags = {}
        for meta in metas:
            _tags = meta['tags']
            for tag in _tags:
                tid,name = tag.split('|')
                if tid not in tags:
                    tags[tid] = {'name':name,'metas':[]}
                tags[tid]['metas'].append(meta)
        return tags

    def date_aggregate(metas):
        dates = {}
        for meta in metas:
            cdate = meta['cdate']
            #raw string
            year,month,day = cdate.split('.')
            if year not in dates:
                dates[year] = {'info':{'name':year,'metas':[]}}
            if month not in dates[year]:
                dates[year][month] = {'name':'.'.join([year,month]),'metas':[]}
            dates[year][month]['metas'].append(meta)
            dates[year]['info']['metas'].append(meta)
        return dates


    agg_info = {}

    #check conflict
    bad_metas,metas = id_conflict(metas)

    agg_info['bad_metas'] = bad_metas
    agg_info['metas'] = metas
    agg_info['catinfo'] = cat_aggregate(metas)
    agg_info['taginfo'] = tag_aggregate(metas)
    agg_info['dateinfo'] = date_aggregate(metas)

    return agg_info


def mvto_article(metas,buildhome):
    article_path = os.path.join(buildhome,__path_article)
    for meta in metas:
        htmlpath = meta['htmlpath']
        fname = '{}.html'.format(meta['fid'])
        fpath = os.path.join(article_path,fname)
        shutil.copy(htmlpath,fpath)


def load_listtemplate(buildhome):
    tmpath = os.path.join(buildhome,__path__template)

    templates = {}
    for fname in os.listdir(tmpath):
        name = fname.strip('.html')
        value = os.path.join(tmpath,fname)
        templates[name] = value

    return templates


def gen_listhtml(info,templatepath,outpath):

    pass


def dispatch_render(agg_info,templates,buildhome):
    
    #only for cat
    cats = agg_info['catinfo']
    for cat in cats:
        info = cats[cat]
        tmpath = templates.get('list.{}.html'.format(cat),'list.default.html')
        outpath = os.path.join(buildhome,cat)
        gen_listhtml(info,tmpath,outpath)



def main(cur_dir=None):

    buildhome = find_buildhome(cur_dir=cur_dir)

    metas,error_metas = load_source_metas(buildhome)

    #error metas 
    for meta in error_metas:
        print('This file is load meta error: ',meta)

    #agg
    agg_info = aggregate_metas(metas)

    #bad metas
    bad_metas = agg_info['bad_metas']
    for meta in bad_metas:
        print('This file conflict',meta['htmlpath'],meta['id'],meta['fid'])


    metas = agg_info['metas']
    #just mv first
    mvto_article(metas,buildhome)

    #render the agginfo
    templates = load_listtemplate(buildhome)

    dispatch_render(agg_info,templates,buildhome)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--gitpath',default=None,action='store',help='give the git path rebuild or jsut this file git')
    args = parser.parse_args()
    cur_dir = args.gitpath
    main(cur_dir=cur_dir)




