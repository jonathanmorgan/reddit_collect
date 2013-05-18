# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Subreddit'
        db.create_table(u'reddit_collect_subreddit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reddit_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('reddit_full_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('display_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('created_dt', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('created_utc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created_utc_dt', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('over_18', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('subscribers', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('public_desc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('header_title', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'reddit_collect', ['Subreddit'])

        # Adding model 'User'
        db.create_table(u'reddit_collect_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reddit_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('reddit_full_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('is_gold', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_mod', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created_dt', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('created_utc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created_utc_dt', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('link_karma', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('comment_karma', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'reddit_collect', ['User'])

        # Adding model 'Post'
        db.create_table(u'reddit_collect_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reddit_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('reddit_full_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reddit_collect.User'], null=True, blank=True)),
            ('author_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('author_reddit_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('domain', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('subreddit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reddit_collect.Subreddit'], null=True, blank=True)),
            ('subreddit_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('subreddit_reddit_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('permalink', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('is_self', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('clicked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('edited', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('saved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('selftext', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('selftext_html', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('num_comments', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('score', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('upvotes', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('downvotes', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('over_18', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created_dt', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('created_utc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created_utc_dt', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('num_reports', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('modhash', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('banned_by', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('approved_by', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('link_flair_class', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('link_flair_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('author_flair_class', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('author_flair_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('comment_collection_status', self.gf('django.db.models.fields.CharField')(default=u'new', max_length=255)),
            ('comments_last_collected', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'reddit_collect', ['Post'])

        # Adding model 'Comment'
        db.create_table(u'reddit_collect_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reddit_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('reddit_full_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('link_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reddit_collect.Comment'], null=True, blank=True)),
            ('parent_reddit_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reddit_collect.User'], null=True, blank=True)),
            ('author_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('author_reddit_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reddit_collect.Post'], null=True, blank=True)),
            ('post_reddit_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('body_html', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('subreddit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reddit_collect.Subreddit'], null=True, blank=True)),
            ('subreddit_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('subreddit_reddit_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('upvotes', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('downvotes', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('score', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created_dt', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('created_utc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created_utc_dt', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('edited', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('edited_dt', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('num_reports', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('modhash', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('banned_by', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('approved_by', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('flair_class', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('flair_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'reddit_collect', ['Comment'])


    def backwards(self, orm):
        # Deleting model 'Subreddit'
        db.delete_table(u'reddit_collect_subreddit')

        # Deleting model 'User'
        db.delete_table(u'reddit_collect_user')

        # Deleting model 'Post'
        db.delete_table(u'reddit_collect_post')

        # Deleting model 'Comment'
        db.delete_table(u'reddit_collect_comment')


    models = {
        u'reddit_collect.comment': {
            'Meta': {'object_name': 'Comment'},
            'approved_by': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reddit_collect.User']", 'null': 'True', 'blank': 'True'}),
            'author_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'author_reddit_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'banned_by': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'body_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_dt': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_utc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_utc_dt': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'downvotes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'edited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'edited_dt': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'flair_class': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'flair_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'link_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'modhash': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'num_reports': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reddit_collect.Comment']", 'null': 'True', 'blank': 'True'}),
            'parent_reddit_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reddit_collect.Post']", 'null': 'True', 'blank': 'True'}),
            'post_reddit_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'reddit_full_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'reddit_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'subreddit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reddit_collect.Subreddit']", 'null': 'True', 'blank': 'True'}),
            'subreddit_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'subreddit_reddit_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'upvotes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'reddit_collect.post': {
            'Meta': {'object_name': 'Post'},
            'approved_by': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reddit_collect.User']", 'null': 'True', 'blank': 'True'}),
            'author_flair_class': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'author_flair_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'author_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'author_reddit_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'banned_by': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'clicked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'comment_collection_status': ('django.db.models.fields.CharField', [], {'default': "u'new'", 'max_length': '255'}),
            'comments_last_collected': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_dt': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_utc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_utc_dt': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'domain': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'downvotes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'edited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_self': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'link_flair_class': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'link_flair_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'modhash': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'num_comments': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_reports': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'over_18': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'permalink': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'reddit_full_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'reddit_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'saved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'selftext': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'selftext_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'subreddit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reddit_collect.Subreddit']", 'null': 'True', 'blank': 'True'}),
            'subreddit_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'subreddit_reddit_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'upvotes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'reddit_collect.subreddit': {
            'Meta': {'object_name': 'Subreddit'},
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'created_dt': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_utc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_utc_dt': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'display_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'header_title': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'over_18': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'public_desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'reddit_full_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'reddit_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'subscribers': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'reddit_collect.user': {
            'Meta': {'object_name': 'User'},
            'comment_karma': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_dt': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_utc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_utc_dt': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_gold': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_mod': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'link_karma': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'reddit_full_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'reddit_id': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['reddit_collect']