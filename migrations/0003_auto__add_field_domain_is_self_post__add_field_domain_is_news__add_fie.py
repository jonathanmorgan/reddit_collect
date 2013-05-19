# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Domain.is_self_post'
        db.add_column(u'reddit_collect_domain', 'is_self_post',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Domain.is_news'
        db.add_column(u'reddit_collect_domain', 'is_news',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Domain.is_multimedia'
        db.add_column(u'reddit_collect_domain', 'is_multimedia',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Domain.use_count'
        db.add_column(u'reddit_collect_domain', 'use_count',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Domain.is_self_post'
        db.delete_column(u'reddit_collect_domain', 'is_self_post')

        # Deleting field 'Domain.is_news'
        db.delete_column(u'reddit_collect_domain', 'is_news')

        # Deleting field 'Domain.is_multimedia'
        db.delete_column(u'reddit_collect_domain', 'is_multimedia')

        # Deleting field 'Domain.use_count'
        db.delete_column(u'reddit_collect_domain', 'use_count')


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
            'domain': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'domain_long_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'domain_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
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