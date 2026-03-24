from django.utils.dateparse import parse_datetime
from .models import Keyword, ContentItem, Flag

class ScannerService:
    def get_mock_data(self):
        return [
            {
                "title": "Learn Django Fast", 
                "body": "Django is a powerful Python framework", 
                "source": "Blog A", 
                "last_updated": "2026-03-20T10:00:00Z"
            },
            {
                "title": "Cooking Tips", 
                "body": "Best recipes for beginners, also learn automation.", 
                "source": "Blog B", 
                "last_updated": "2026-03-20T10:00:00Z"
            },
            {
                "title": "python", 
                "body": "Python is a great programming language.", 
                "source": "News D", 
                "last_updated": "2026-03-21T10:00:00Z"
            }
        ]

    def run(self):
        data = self.get_mock_data()
        keywords = Keyword.objects.all()
        flags_created = 0

        for item_data in data:
            # 1. ContentItem ko Database me Save ya Update karna
            last_updated_dt = parse_datetime(item_data['last_updated'])
            
            # Agar isi title aur source ka content pehle se hai, to bas body update karo, warna naya banao
            content_item, created = ContentItem.objects.update_or_create(
                title=item_data['title'],
                source=item_data['source'],
                defaults={
                    'body': item_data['body'],
                    'last_updated': last_updated_dt
                }
            )

            # 2. Har Keyword ko is content item ke sath match karna
            for keyword in keywords:
                kw = keyword.name.lower()
                title = content_item.title.lower()
                body = content_item.body.lower()

                score = 0
                
                # --- MATCHING LOGIC (Assignment Requirement #4) ---
                if kw == title:
                    score = 100  # Exact match in title
                elif kw in title:
                    score = 70   # Partial match in title
                elif kw in body:
                    score = 40   # Match only in body
                
                if score > 0:
                    # Check karna ki kya ye Flag pehle se bana hua hai?
                    existing_flag = Flag.objects.filter(keyword=keyword, content_item=content_item).first()
                    
                    if existing_flag:
                        # --- SUPPRESSION LOGIC (Assignment Requirement #6) ---
                        if existing_flag.status == 'irrelevant':
                            # Agar flag 'irrelevant' tha, to tab tak ignore karo jab tak content update na hua ho
                            if content_item.last_updated > existing_flag.updated_at:
                                # Content update ho gaya! Flag ko reset karke wapas active karo
                                existing_flag.status = 'pending'
                                existing_flag.score = score
                                existing_flag.save()
                                flags_created += 1
                        else:
                            # Agar pending/relevant hai to bas score update karo agar zaroorat ho
                            existing_flag.score = score
                            existing_flag.save()
                    else:
                        # Naya Flag generate karna
                        Flag.objects.create(
                            keyword=keyword,
                            content_item=content_item,
                            score=score,
                            status='pending'
                        )
                        flags_created += 1

        return flags_created
