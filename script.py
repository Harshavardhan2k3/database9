#!/usr/bin/env python3

import requests
import random
import time
import threading
import logging
import sys
from collections import namedtuple

# --- SCRIPT CONFIGURATION ---

# 1. Test Parameters (Global Variables)
TOTAL_REQUESTS = 20000
MAX_WORKERS = 200
# 2. URL and Headers (as specified in the request)
FULL_URL_TEMPLATE = "https://stbavheyxshbpnmbviys.supabase.co/rest/v1/looms?select={RANDOM_PARAMS}&title=ilike.{like_expression}&limit={random_limit_between_30_to_300}"

HEADERS = {
    "Host": "stbavheyxshbpnmbviys.supabase.co",
    "X-Client-Info": "supabase-js-web/2.96.0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
    "Apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN0YmF2aGV5eHNoYnBubWJ2aXlzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIxNzYyNjMsImV4cCI6MjA3Nzc1MjI2M30.WgJPWkZyblPzydeclDsxfLDVDdGdCQWwphLxJ4BM7Gs",
    "Accept": "*/*",
    "Origin": "https://www.knitt.app",
    "Sec-Fetch-Site": "cross-site",
    "Cache-Control": "no-cache, no-store, must-revalidate",
    "pragma": "no-cache",
    "Connection": "close",
    "Expires": "0",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://www.knitt.app/",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=0, i"
}

# 3. Randomization Lists (as specified)
random_params_list = [
    "id%2Ctitle", "description%2Ctag%2Ccreated_by", "poster_url%2Cmember_count%2Ctitle",
    "pre_rating_avg%2Cpre_rating_count%2Cid%2Ctitle", "post_rating_avg%2Cpost_rating_count%2Ccreated_at",
    "updated_at%2Cid%2Cdescription%2Ctag", "loom_movies%28movie_id%2Ctitle_color%29%2Cid",
    "loom_people%28person_id%2Ctitle_color%29%2Ctitle%2Ccreated_by", "id%2Cposter_url%2Cmember_count%2Ccreated_at%2Cupdated_at",
    "title%2Cdescription%2Ctag%2Cpre_rating_avg%2Cpost_rating_avg", "created_by%2Cposter_url%2Cpre_rating_count%2Cpost_rating_count",
    "id%2Ctitle%2Cdescription%2Ccreated_at%2Cupdated_at%2Cmember_count",
    "loom_movies%28movie_id%2Ctitle_color%29%2Cloom_people%28person_id%2Ctitle_color%29",
    "title%2Ctag%2Cposter_url%2Cpre_rating_avg%2Cpre_rating_count%2Cpost_rating_avg",
    "id%2Ccreated_by%2Cmember_count%2Cpost_rating_count%2Cupdated_at",
    "description%2Ctag%2Ccreated_by%2Cposter_url%2Cmember_count%2Cpre_rating_avg%2Cpre_rating_count",
    "title%2Cdescription%2Cloom_movies%28movie_id%2Ctitle_color%29%2Ccreated_at%2Cupdated_at",
    "id%2Ctitle%2Ctag%2Cpre_rating_avg%2Cpost_rating_avg%2Cloom_people%28person_id%2Ctitle_color%29",
    "id%2Cdescription", "title%2Ccreated_by", "tag%2Cposter_url", "member_count%2Ccreated_at",
    "updated_at%2Cpost_rating_avg", "pre_rating_count%2Cpost_rating_count", "id%2Ctag%2Cmember_count",
    "title%2Cposter_url%2Ccreated_at", "description%2Cpre_rating_avg%2Cupdated_at",
    "created_by%2Cpost_rating_avg%2Cpost_rating_count", "id%2Ctitle%2Cmember_count%2Cpost_rating_avg",
    "tag%2Cposter_url%2Cpre_rating_count%2Ccreated_at", "description%2Ccreated_by%2Cmember_count%2Cupdated_at",
    "title%2Cpre_rating_avg%2Cpre_rating_count%2Cpost_rating_count",
    "id%2Cposter_url%2Cpre_rating_avg%2Ccreated_at%2Cupdated_at",
    "created_by%2Cmember_count%2Cpre_rating_count%2Cpost_rating_avg%2Cupdated_at",
    "loom_movies%28movie_id%2Ctitle_color%29%2Ctitle%2Cpost_rating_avg",
    "loom_people%28person_id%2Ctitle_color%29%2Cdescription%2Cpre_rating_count"
]

search_terms = [
    '0','00','01','02','03','04','05','06','07','08','09','1','10','11','12','13','14','15','16','17','18','19',
    '2','20','21','22','23','24','25','26','27','28','29','3','30','31','32','33','34','35','36','37','38','39',
    '4','40','41','42','43','44','45','46','47','48','49','5','50','51','52','53','54','55','56','57','58','59',
    '6','60','61','62','63','64','65','66','67','68','69','7','70','71','72','73','74','75','76','77','78','79',
    '8','80','81','82','83','84','85','86','87','88','89','9','90','91','92','93','94','95','96','97','98','99',
    'a','aa','ab','ac','ad','ae','af','ag','ah','ai','aj','ak','al','am','an','ao','ap','aq','ar','as','at','au','av','aw','ax','ay','az',
    'b','ba','bb','bc','bd','be','bf','bg','bh','bi','bj','bk','bl','bm','bn','bo','bp','bq','br','bs','bt','bu','bv','bw','bx','by','bz',
    'c','ca','cb','cc','cd','ce','cf','cg','ch','ci','cj','ck','cl','cm','cn','co','cp','cq','cr','cs','ct','cu','cv','cw','cx','cy','cz',
    'd','da','db','dc','dd','de','df','dg','dh','di','dj','dk','dl','dm','dn','do','dp','dq','dr','ds','dt','du','dv','dw','dx','dy','dz',
    'e','ea','eb','ec','ed','ee','ef','eg','eh','ei','ej','ek','el','em','en','eo','ep','eq','er','es','et','eu','ev','ew','ex','ey','ez',
    'f','fa','fb','fc','fd','fe','ff','fg','fh','fi','fj','fk','fl','fm','fn','fo','fp','fq','fr','fs','ft','fu','fv','fw','fx','fy','fz',
    'g','ga','gb','gc','gd','ge','gf','gg','gh','gi','gj','gk','gl','gm','gn','go','gp','gq','gr','gs','gt','gu','gv','gw','gx','gy','gz',
    'h','ha','hb','hc','hd','he','hf','hg','hh','hi','hj','hk','hl','hm','hn','ho','hp','hq','hr','hs','ht','hu','hv','hw','hx','hy','hz',
    'i','ia','ib','ic','id','ie','if','ig','ih','ii','ij','ik','il','im','in','io','ip','iq','ir','is','it','iu','iv','iw','ix','iy','iz',
    'j','ja','jb','jc','jd','je','jf','jg','jh','ji','jj','jk','jl','jm','jn','jo','jp','jq','jr','js','jt','ju','jv','jw','jx','jy','jz',
    'k','ka','kb','kc','kd','ke','kf','kg','kh','ki','kj','kk','kl','km','kn','ko','kp','kq','kr','ks','kt','ku','kv','kw','kx','ky','kz',
    'l','la','lb','lc','ld','le','lf','lg','lh','li','lj','lk','ll','lm','ln','lo','lp','lq','lr','ls','lt','lu','lv','lw','lx','ly','lz',
    'm','ma','mb','mc','md','me','mf','mg','mh','mi','mj','mk','ml','mm','mn','mo','mp','mq','mr','ms','mt','mu','mv','mw','mx','my','mz',
    'n','na','nb','nc','nd','ne','nf','ng','nh','ni','nj','nk','nl','nm','nn','no','np','nq','nr','ns','nt','nu','nv','nw','nx','ny','nz',
    'o','oa','ob','oc','od','oe','of','og','oh','oi','oj','ok','ol','om','on','oo','op','oq','or','os','ot','ou','ov','ow','ox','oy','oz',
    'p','pa','pb','pc','pd','pe','pf','pg','ph','pi','pj','pk','pl','pm','pn','po','pp','pq','pr','ps','pt','pu','pv','pw','px','py','pz',
    'q','qa','qb','qc','qd','qe','qf','qg','qh','qi','qj','qk','ql','qm','qn','qo','qp','qq','qr','qs','qt','qu','qv','qw','qx','qy','qz',
    'r','ra','rb','rc','rd','re','rf','rg','rh','ri','rj','rk','rl','rm','rn','ro','rp','rq','rr','rs','rt','ru','rv','rw','rx','ry','rz',
    's','sa','sb','sc','sd','se','sf','sg','sh','si','sj','sk','sl','sm','sn','so','sp','sq','sr','ss','st','su','sv','sw','sx','sy','sz',
    't','ta','tb','tc','td','te','tf','tg','th','ti','tj','tk','tl','tm','tn','to','tp','tq','tr','ts','tt','tu','tv','tw','tx','ty','tz',
    'u','ua','ub','uc','ud','ue','uf','ug','uh','ui','uj','uk','ul','um','un','uo','up','uq','ur','us','ut','uu','uv','uw','ux','uy','uz',
    'v','va','vb','vc','vd','ve','vf','vg','vh','vi','vj','vk','vl','vm','vn','vo','vp','vq','vr','vs','vt','vu','vv','vw','vx','vy','vz',
    'w','wa','wb','wc','wd','we','wf','wg','wh','wi','wj','wk','wl','wm','wn','wo','wp','wq','wr','ws','wt','wu','wv','ww','wx','wy','wz',
    'x','xa','xb','xc','xd','xe','xf','xg','xh','xi','xj','xk','xl','xm','xn','xo','xp','xq','xr','xs','xt','xu','xv','xw','xx','xy','xz',
    'y','ya','yb','yc','yd','ye','yf','yg','yh','yi','yj','yk','yl','ym','yn','yo','yp','yq','yr','ys','yt','yu','yv','yw','yx','yy','yz',
    'z','za','zb','zc','zd','ze','zf','zg','zh','zi','zj','zk','zl','zm','zn','zo','zp','zq','zr','zs','zt','zu','zv','zw','zx','zy','zz'
]

# %25 is the URL encoding for the '%' character.
like_expression_formats = ["%25{search_term_here}", "%25{search_term_here}%25", "{search_term_here}%25", "{search_term_here}"]

# For storing results safely from multiple threads
Result = namedtuple('Result', ['status_code', 'duration_s', 'error'])
results = []
# A lock to protect writing to the results list
results_lock = threading.Lock()

# --- LOGGING SETUP ---
def setup_logging():
    """Configures logging to console only."""
    log_formatter = logging.Formatter(
        '%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s'
    )
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    root_logger.addHandler(console_handler)

# --- CORE LOGIC ---

def build_random_url():
    """Constructs a URL with random parameters based on the defined lists."""
    random_params = random.choice(random_params_list)
    search_term = random.choice(search_terms)
    like_format = random.choice(like_expression_formats)
    like_expression = like_format.format(search_term_here=search_term)
    random_limit = random.randint(30, 300)

    # Fill the template with the chosen random values
    return FULL_URL_TEMPLATE.format(
        RANDOM_PARAMS=random_params,
        like_expression=like_expression,
        random_limit_between_30_to_300=random_limit
    )

def make_request(worker_id, stop_event):
    """The main function for each thread. Continuously makes requests until stop_event is set."""
    logging.info(f"Worker {worker_id} started.")
    session = requests.Session()  # Use a session for potential connection pooling

    while not stop_event.is_set():
        url = build_random_url()
        start_time = time.monotonic()
        
        try:
            response = session.get(url, headers=HEADERS, timeout=15) # 15-second timeout
            duration = time.monotonic() - start_time
            
            # Check for HTTP errors (4xx or 5xx)
            if 400 <= response.status_code < 600:
                logging.error(
                    f"Worker {worker_id}: HTTP Error {response.status_code} for URL: {url} | "
                    f"Response: {response.text[:200]}"
                )
                result = Result(response.status_code, duration, response.text)
            else:
                # To avoid flooding the console, we only log errors and a few successes
                if random.randint(1, 100) == 1: # Log 1% of successes
                    logging.info(
                        f"Worker {worker_id}: SUCCESS (Status: {response.status_code}, Time: {duration:.2f}s) URL: {url}"
                    )
                result = Result(response.status_code, duration, None)

        except requests.exceptions.RequestException as e:
            duration = time.monotonic() - start_time
            logging.error(f"Worker {worker_id}: Request failed for URL: {url} | Error: {e}", exc_info=False)
            result = Result(None, duration, str(e))
        
        # Safely append result to the shared list
        with results_lock:
            results.append(result)

    logging.info(f"Worker {worker_id} stopping.")

def analyze_results():
    """Calculates and prints a summary of the test results."""
    logging.info("--- TEST RESULTS ---")
    
    if not results:
        logging.warning("No results were recorded.")
        return

    # Use a local copy to avoid race conditions if any threads are still writing
    with results_lock:
        final_results = list(results)
        
    total_requests_made = len(final_results)
    success_requests = [r for r in final_results if r.status_code is not None and 200 <= r.status_code < 400]
    failed_requests = [r for r in final_results if r not in success_requests]

    num_success = len(success_requests)
    num_failed = len(failed_requests)

    success_rate = (num_success / total_requests_made) * 100 if total_requests_made > 0 else 0
    
    # Final summary output
    sys.stdout.write("\n") # Move to next line after progress bar
    sys.stdout.flush()
    
    print("\n" + "="*50)
    print("                 LOAD TEST SUMMARY")
    print("="*50)
    print(f"Total Requests Made: {total_requests_made}")
    print(f"Successful Requests: {num_success} ({success_rate:.2f}%)")
    print(f"Failed Requests:     {num_failed} ({100 - success_rate:.2f}%)")

    if success_requests:
        response_times = [r.duration_s for r in success_requests]
        avg_time = sum(response_times) / len(response_times)
        max_time = max(response_times)
        min_time = min(response_times)
        
        # Calculate 95th percentile
        response_times.sort()
        p95_index = int(len(response_times) * 0.95)
        p95_time = response_times[p95_index]

        print("\n--- Response Time Stats (for successful requests) ---")
        print(f"Average: {avg_time:.3f} s")
        print(f"Min:     {min_time:.3f} s")
        print(f"Max:     {max_time:.3f} s")
        print(f"95th P:  {p95_time:.3f} s")
    
    print("="*50)
    logging.info("Analysis complete.")


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    setup_logging()
    
    print("="*80)
    print("                      PYTHON LOAD & STRESS TESTER")
    print("="*80)
    logging.info("Execution State: START")
    logging.info(f"Test Configuration: {MAX_WORKERS} concurrent workers, aiming for {TOTAL_REQUESTS} total requests.")
    logging.info("Logging is configured for console output only.")
    print("="*80)

    stop_event = threading.Event()
    threads = []
    
    start_time = time.monotonic()

    # Create and start worker threads
    for i in range(MAX_WORKERS):
        thread = threading.Thread(
            target=make_request,
            name=f"Worker-{i+1}",
            args=(i + 1, stop_event)
        )
        thread.daemon = True # Allows main thread to exit even if workers are blocking
        threads.append(thread)
        thread.start()

    # Monitor progress and stop when the target is reached
    try:
        while len(results) < TOTAL_REQUESTS:
            progress = len(results)
            percentage = (progress / TOTAL_REQUESTS) * 100
            # \r moves the cursor to the beginning of the line
            sys.stdout.write(f"\rProgress: {progress}/{TOTAL_REQUESTS} requests ({percentage:.2f}%) completed...")
            sys.stdout.flush()
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        logging.warning("\nKeyboard interrupt received. Stopping workers early...")
    
    finally:
        # Final progress update
        progress = len(results)
        percentage = min(100.00, (progress / TOTAL_REQUESTS) * 100)
        sys.stdout.write(f"\rProgress: {progress}/{TOTAL_REQUESTS} requests ({percentage:.2f}%) completed...\n")
        sys.stdout.flush()

        # Signal all threads to stop
        logging.info("Request target met or interrupted. Signaling workers to stop...")
        stop_event.set()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        total_duration = time.monotonic() - start_time
        logging.info(f"All workers have stopped. Total test time: {total_duration:.2f} seconds.")
        logging.info("Execution State: END")
        
        # Analyze and print the final results

        analyze_results()
