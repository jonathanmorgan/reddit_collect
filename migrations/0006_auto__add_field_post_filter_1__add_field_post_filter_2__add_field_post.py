# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Post.filter_1'
        db.add_column(u'reddit_collect_post', 'filter_1',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Post.filter_2'
        db.add_column(u'reddit_collect_post', 'filter_2',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Post.filter_3'
        db.add_column(u'reddit_collect_post', 'filter_3',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Post.filter_4'
        db.add_column(u'reddit_collect_post', 'filter_4',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Post.filter_5'
        db.add_column(u'reddit_collect_post', 'filter_5',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Post.filter_6'
        db.add_column(u'reddit_collect_post', 'filter_6',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Post.filter_7'
        db.add_column(u'reddit_collect_post', 'filter_7',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Post.filter_8'
        db.add_column(u'reddit_collect_post', 'filter_8',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Post.filter_9'
        db.add_column(u'reddit_collect_post', 'filter_9',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Post.filter_10'
        db.add_column(u'reddit_collect_post', 'filter_10',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Post.filter_1'
        db.delete_column(u'reddit_collect_post', 'filter_1')

        # Deleting field 'Post.filter_2'
        db.delete_column(u'reddit_collect_post', 'filter_2')

        # Deleting field 'Post.filter_3'
        db.delete_column(u'reddit_collect_post', 'filter_3')

        # Deleting field 'Post.filter_4'
        db.delete_column(u'reddit_collect_post', 'filter_4')

        # Deleting field 'Post.filter_5'
        db.delete_column(u'reddit_collect_post', 'filter_5')

        # Deleting field 'Post.filter_6'
        db.delete_column(u'reddit_collect_post', 'filter_6')

        # Deleting field 'Post.filter_7'
        db.delete_column(u'reddit_collect_post', 'filter_7')

        # Deleting field 'Post.filter_8'
        db.delete_column(u'reddit_collect_post', 'filter_8')

        # Deleting field 'Post.filter_9'
        db.delete_column(u'reddit_collect_post', 'filter_9')

        # Deleting field 'Post.filter_10'
        db.delete_column(u'reddit_collect_post', 'filter_10')


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
            'reddit_full_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'reddit_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'subreddit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reddit_collect.Subreddit']", 'null': 'True', 'blank': 'True'}),
            'subreddit_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'subreddit_reddit_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'upvotes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'reddit_collect.domain': {
            'Meta': {'object_name': 'Domain'},
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_multimedia': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_news': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_self_post': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'long_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'use_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
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
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reddit_collect.Domain']", 'null': 'True', 'blank': 'True'}),
            'domain_long_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'domain_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'downvotes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'edited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'filter_1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'filter_10': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'filter_2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'filter_3': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'filter_4': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'filter_5': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'filter_6': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'filter_7': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'filter_8': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'filter_9': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'reddit_full_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'reddit_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'saved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'selftext': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'selftext_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'subreddit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reddit_collect.Subreddit']", 'null': 'True', 'blank': 'True'}),
            'subreddit_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'subreddit_reddit_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
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