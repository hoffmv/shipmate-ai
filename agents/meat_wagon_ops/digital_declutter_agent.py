import datetime
from collections import defaultdict
from typing import List, Dict, Any


class DigitalDeclutterAgent:
    """
    DigitalDeclutterAgent analyzes digital environments for clutter and recommends cleanup actions.
    """

    # Thresholds and settings
    OLD_FILE_DAYS = 180  # Files older than this are considered for archive/delete
    LARGE_FILE_MB = 500  # Files larger than this are considered large
    UNUSED_APP_LIST = [
        'Calculator', 'Notepad', 'Paint', 'Sticky Notes', 'Calendar'
    ]  # Example of apps often left open but rarely used
    TEMP_FILE_TYPES = {'tmp', 'temp', 'log', 'cache'}
    ARCHIVE_FILE_TYPES = {'zip', 'rar', '7z', 'tar', 'gz', 'archive'}
    DOCUMENT_FILE_TYPES = {'doc', 'docx', 'pdf', 'ppt', 'pptx', 'xls', 'xlsx', 'txt'}
    IMAGE_FILE_TYPES = {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'svg'}
    VIDEO_FILE_TYPES = {'mp4', 'mov', 'avi', 'mkv', 'wmv'}
    DUPLICATE_NAME_CONFIDENCE = 0.9
    OLD_FILE_CONFIDENCE = 0.8
    LARGE_FILE_CONFIDENCE = 0.7
    TEMP_FILE_CONFIDENCE = 1.0
    UNUSED_APP_CONFIDENCE = 0.85
    REDUNDANT_TAB_CONFIDENCE = 0.95

    def analyze(self, input: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        files = input.get('file_scan', [])
        tabs = input.get('tab_list', [])
        open_apps = input.get('open_apps', [])

        file_recs = self._analyze_files(files)
        tab_recs = self._analyze_tabs(tabs)
        app_recs = self._analyze_apps(open_apps)

        return {
            'files': file_recs,
            'tabs': tab_recs,
            'apps': app_recs
        }

    def _analyze_files(self, files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        now = datetime.datetime.utcnow()
        file_by_name = defaultdict(list)
        recs = []

        # Group files by name for duplicate detection
        for f in files:
            file_by_name[f['name'].lower()].append(f)

        for f in files:
            name = f['name']
            path = f['path']
            last_modified = f['last_modified']
            size = f.get('size_in_mb', 0)
            ftype = f.get('type', '').lower()

            # Parse last_modified
            try:
                lm_dt = datetime.datetime.fromisoformat(last_modified)
            except Exception:
                # If parsing fails, treat as old
                lm_dt = now - datetime.timedelta(days=self.OLD_FILE_DAYS + 1)

            age_days = (now - lm_dt).days

            # 1. Temporary files
            if ftype in self.TEMP_FILE_TYPES or name.lower().endswith('.tmp'):
                recs.append({
                    'name': name,
                    'path': path,
                    'action': 'delete',
                    'confidence': self.TEMP_FILE_CONFIDENCE,
                    'reason': 'Temporary file type detected; safe to delete.'
                })
                continue

            # 2. Duplicate files (same name, different path)
            duplicates = file_by_name[name.lower()]
            if len(duplicates) > 1:
                # Keep the most recently modified, suggest archive/delete others
                most_recent = max(duplicates, key=lambda x: x['last_modified'])
                if f is not most_recent:
                    recs.append({
                        'name': name,
                        'path': path,
                        'action': 'archive',
                        'confidence': self.DUPLICATE_NAME_CONFIDENCE,
                        'reason': 'Duplicate file detected; consider archiving older copy.'
                    })
                    continue

            # 3. Old files
            if age_days > self.OLD_FILE_DAYS:
                if ftype in self.DOCUMENT_FILE_TYPES or ftype in self.IMAGE_FILE_TYPES or ftype in self.VIDEO_FILE_TYPES:
                    recs.append({
                        'name': name,
                        'path': path,
                        'action': 'archive',
                        'confidence': self.OLD_FILE_CONFIDENCE,
                        'reason': f'File has not been modified in over {self.OLD_FILE_DAYS} days.'
                    })
                elif ftype in self.ARCHIVE_FILE_TYPES:
                    recs.append({
                        'name': name,
                        'path': path,
                        'action': 'delete',
                        'confidence': self.OLD_FILE_CONFIDENCE,
                        'reason': f'Old archive file; likely no longer needed.'
                    })
                else:
                    recs.append({
                        'name': name,
                        'path': path,
                        'action': 'archive',
                        'confidence': self.OLD_FILE_CONFIDENCE - 0.1,
                        'reason': f'File is old; consider archiving.'
                    })
                continue

            # 4. Large files
            if size >= self.LARGE_FILE_MB:
                recs.append({
                    'name': name,
                    'path': path,
                    'action': 'archive',
                    'confidence': self.LARGE_FILE_CONFIDENCE,
                    'reason': f'Large file (>={self.LARGE_FILE_MB} MB); consider archiving to save space.'
                })
                continue

            # 5. Old archive files
            if ftype in self.ARCHIVE_FILE_TYPES and age_days > 30:
                recs.append({
                    'name': name,
                    'path': path,
                    'action': 'delete',
                    'confidence': self.OLD_FILE_CONFIDENCE,
                    'reason': 'Archive file is older than 30 days; likely safe to delete.'
                })
                continue

            # 6. Otherwise, ignore
            recs.append({
                'name': name,
                'path': path,
                'action': 'ignore',
                'confidence': 0.99,
                'reason': 'No clutter detected for this file.'
            })

        return recs

    def _analyze_tabs(self, tabs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        seen_urls = set()
        recs = []
        url_counts = defaultdict(int)

        # Count occurrences for redundancy
        for tab in tabs:
            url = tab.get('url', '').strip().lower()
            url_counts[url] += 1

        for tab in tabs:
            url = tab.get('url', '').strip().lower()
            title = tab.get('title', '').strip()
            if not url:
                continue

            # 1. Redundant tabs (same URL open multiple times)
            if url_counts[url] > 1:
                if url in seen_urls:
                    recs.append({
                        'url': url,
                        'action': 'close',
                        'confidence': self.REDUNDANT_TAB_CONFIDENCE,
                        'reason': 'Duplicate tab detected; safe to close.'
                    })
                    continue
                else:
                    seen_urls.add(url)
                    recs.append({
                        'url': url,
                        'action': 'keep',
                        'confidence': 0.99,
                        'reason': 'First instance of this tab; keep open.'
                    })
                    continue

            # 2. Tabs with generic titles (e.g., "New Tab", "Untitled")
            if title.lower() in {'new tab', 'untitled', ''}:
                recs.append({
                    'url': url,
                    'action': 'close',
                    'confidence': 0.8,
                    'reason': 'Tab appears unused or blank.'
                })
                continue

            # 3. Otherwise, keep
            recs.append({
                'url': url,
                'action': 'keep',
                'confidence': 0.99,
                'reason': 'No clutter detected for this tab.'
            })

        return recs

    def _analyze_apps(self, open_apps: List[str]) -> List[Dict[str, Any]]:
        recs = []
        app_counts = defaultdict(int)
        for app in open_apps:
            app_counts[app.lower()] += 1

        for app in open_apps:
            app_lower = app.lower()

            # 1. Unused/utility apps
            if app in self.UNUSED_APP_LIST:
                recs.append({
                    'name': app,
                    'action': 'close',
                    'confidence': self.UNUSED_APP_CONFIDENCE,
                    'reason': 'Utility app often left open unintentionally.'
                })
                continue

            # 2. Duplicate app instances (rare, but possible)
            if app_counts[app_lower] > 1:
                recs.append({
                    'name': app,
                    'action': 'close',
                    'confidence': 0.9,
                    'reason': 'Multiple instances of this app detected; consider closing extras.'
                })
                app_counts[app_lower] -= 1
                continue

            # 3. Otherwise, keep
            recs.append({
                'name': app,
                'action': 'keep',
                'confidence': 0.99,
                'reason': 'No clutter detected for this app.'
            })

        return recs