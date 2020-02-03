from apps.photologue_ladiaria.models import PhotoExtended, Photographer as pl_photographer, Agency as pl_agency
from apps.photologue.models import Photographer as p_photographer, Agency as p_agency
from apps.core.models import Article, ArticleBodyImage, Category, Publication
import json
from django.db import transaction
from apps.photologue.models import Photo as p_photo
from photologue.models import Photo


def loaddata():
    data = None
    categories = None
    articles = None
    article_body_images = None
    publications = None
    with open("migration_data.json", buffering=1000000, mode="r") as read_file:
        data = json.load(read_file)
        publications = [item for item in data if item['model'] == 'core.publication']
        articles = [item for item in data if item['model'] == 'core.article']
        article_body_images = [item for item in data if item['model'] == 'core.articlebodyimage']
        categories = [item for item in data if item['model'] == 'core.category']
        count = 1
        art = 1
        with transaction.commit_on_success():
            for item in data:
                new_agency = None
                new_photograper = None
                if item['model'] == 'photologue.photo':
                    print '*' * 100 + str(item) + '*' * 100
                    photo = p_photo.objects.get(id=item['pk'])
                    # photo = Photo.objects.create(
                    #     title=photo.title, title_slug=photo.title_slug,
                    #     caption=photo.caption, date_added=photo.date_added, is_public=photo.is_public, tags=photo.tags)
                    old_photographer = p_photographer.objects.get(id=item['fields']['photographer']) \
                        if item['fields']['photographer'] is not None else None
                    if old_photographer is not None:
                        print old_photographer.name + 'l'*100
                        new_photograper, created = pl_photographer.objects.get_or_create(name=old_photographer.name,
                         defaults={
                             'name': old_photographer.name,
                             'email': old_photographer.email,
                             'date_created': old_photographer.date_created
                         })
                    old_agency = p_agency.objects.get(id=item['fields']['agency']) \
                        if item['fields']['agency'] is not None else None
                    if old_agency is not None:
                        new_agency, created = pl_agency.objects.get_or_create(name=old_agency.name,
                                                                              defaults={'name': old_agency.name,
                                                                                        'info': old_agency.info,
                                                                                        'date_created': old_agency.date_created}
                                                                              )
                    photo_extended, created = PhotoExtended.objects.get_or_create(image=photo,
                                                                                  defaults={'image': photo,
                                                                                            'agency': new_agency,
                                                                                            'photographer': new_photograper})
                    # photo_extended = PhotoExtended(image=photo, agency=new_agency, photographer=new_photograper)
                    # category begin
                    # pk = None
                    # for c in categories:
                    #     if c['fields']['full_width_cover_image'] == photo.id:
                    #         pk = c['pk']
                    #         category = Category.objects.get(pk=pk)
                    #         try:
                    #             photo_extended.category_set.add(category)
                    #         except:
                    #             print 'c'*100, category, 'c'*100
                    #             break
                    #         break
                    # # category end
                    # # article begin
                    pk = None
                    for a in articles:
                        if a['fields']['photo'] == photo.id:
                            pk = a['pk']
                            article = Article.objects.get(pk=pk)
                            photo_extended.article_set.add(article)
                            break
                    # article end
                    # publication begin
                    # pk = None
                    # for p in publications:
                    #     if p['fields']['full_width_cover_image'] == photo.id:
                    #         pk = p['pk']
                    #         publication = Publication.objects.get(pk=pk)
                    #         photo_extended.publication_set.add(publication)
                    #         break
                    # # publication end
                    # # ArticleBodyImage begin
                    # pk = None
                    # for abi in article_body_images:
                    #     if abi['fields']['image'] == photo.id:
                    #         pk = abi['pk']
                    #         articlebodyimage = ArticleBodyImage.objects.get(pk=pk)
                    #         photo_extended.photo.add(articlebodyimage)
                    #         break
                    # # ArticleBodyImage end
                    photo_extended.save()
                    print 'photo_extended numero ' + str(count) + ' salvado' + '*' * 100
                    count += 1
                    art += 1

        # ./manage.py dumpdata photologue.Photo photologue.Photographer photologue.Agency core.Article core.ArticleBodyImage --indent 2 > migration_data.json


loaddata()

# photo_extends = []
#     with transaction.commit_on_success():
#         custome_photologue = Photo.objects.all()
#         for cp in custome_photologue:
#             photo_extended = PhotoExtended(
#                 image=cp, agency=cp.agency, photographer=cp.photographer)
#             photo_extended.category_set.add(cp.category_set.all())
#             photo_extended.article_set.add(cp.article_set.all())
#             photo_extended.publication_set.add(cp.publication_set.all())
#             photo_extended.photo_set.add(cp.photo_set.all())
#             photo_extends.append(photo_extended)
#         PhotoExtended.objects.bulk_create(photo_extends)
